#!/usr/bin/env python3
"""
Telegram Bot для автоматической персонализированной воронки анонсов
"""

import asyncio
import argparse
import os
import sys
from pathlib import Path

from aiogram import Bot
from aiogram.types import FSInputFile
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError

from utils import load_users, render_html, html_to_png, get_keyboard, get_random_variant
from config import BOT_TOKEN, STAGES, SEND_DELAY, VARIANTS


async def send_funnel(bot: Bot, users_df, output_dir: str, send_real: bool = False, variant_mode: str = 'fixed'):
    """
    Отправляет персонализированную воронку пользователям с поддержкой A/B-тестирования
    """
    print(f"Начинаем обработку {len(users_df)} пользователей...")
    print(f"Режим: {'Отправка' if send_real else 'Тестирование (генерация PNG)'}")
    print(f"Варианты: {variant_mode}")
    
    total_messages = len(users_df) * len(STAGES)
    processed = 0
    variant_stats = {'a': 0, 'b': 0, 'c': 0}
    
    for _, row in users_df.iterrows():
        user_data = {
            'name': row['name'],
            'role': row['role'],
            'company': row['company']
        }
        chat_id = row['telegram_id']
        
        # Определяем вариант для пользователя
        if variant_mode == 'random':
            variant = get_random_variant()
        else:
            variant = row.get('variant', 'a')
        
        print(f"\nОбрабатываем пользователя: {user_data['name']} (ID: {chat_id}, вариант: {variant.upper()})")
        
        for stage in STAGES:
            try:
                # Рендерим HTML с учетом варианта
                html_content = render_html(stage, variant, user_data)
                
                # Конвертируем в PNG с уникальным именем
                png_path = html_to_png(html_content, f"{stage}_{variant}", chat_id, output_dir, user_data)
                
                if send_real:
                    # Отправляем через бота
                    keyboard = get_keyboard(stage, chat_id, user_data['name'])
                    caption = f"Этап {stage.capitalize()} (вариант {variant.upper()}) для {user_data['name']}"
                    
                    try:
                        await bot.send_photo(
                            chat_id=chat_id,
                            photo=FSInputFile(png_path),
                            caption=caption,
                            reply_markup=keyboard
                        )
                        print(f"✅ Отправлено: {stage}_{variant} для {user_data['name']}")
                        
                    except TelegramBadRequest as e:
                        print(f"❌ Ошибка отправки {stage}_{variant} для {user_data['name']}: {e}")
                    except TelegramForbiddenError as e:
                        print(f"❌ Пользователь {user_data['name']} заблокировал бота: {e}")
                    except Exception as e:
                        print(f"❌ Неожиданная ошибка при отправке {stage}_{variant} для {user_data['name']}: {e}")
                    
                    # Задержка между отправками
                    await asyncio.sleep(SEND_DELAY)
                else:
                    print(f"📸 Сгенерирован: {png_path}")
                
                # Статистика вариантов
                variant_stats[variant] += 1
                processed += 1
                print(f"Прогресс: {processed}/{total_messages}")
                
            except Exception as e:
                print(f"❌ Ошибка при обработке {stage}_{variant} для {user_data['name']}: {e}")
                continue
    
    print(f"\n🎉 Обработка завершена! Обработано {processed} сообщений.")
    print(f"📊 Статистика вариантов: {variant_stats}")


async def main():
    """Основная функция"""
    parser = argparse.ArgumentParser(description='Telegram Bot для воронки анонсов с A/B-тестированием')
    parser.add_argument('--test', action='store_true', help='Тестовый режим (только генерация PNG)')
    parser.add_argument('--send', action='store_true', help='Режим отправки сообщений')
    parser.add_argument('--variant', choices=['fixed', 'random'], default='fixed', 
                       help='Режим выбора вариантов: fixed (по CSV) или random (случайно)')
    
    args = parser.parse_args()
    
    # Определяем режим работы
    if args.send:
        send_real = True
        mode = "отправки"
    else:
        send_real = False
        mode = "тестирования"
    
    print(f"🚀 Запуск в режиме {mode}")
    print(f"🎯 Варианты: {args.variant}")
    
    # Проверяем токен бота
    if not BOT_TOKEN:
        print("❌ Ошибка: BOT_TOKEN не найден в переменных окружения")
        print("Создайте файл .env и добавьте BOT_TOKEN=your_bot_token")
        sys.exit(1)
    
    # Создаем директорию для вывода
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Загружаем пользователей
        users_df = load_users('users.csv')
        
        if users_df.empty:
            print("❌ Ошибка: CSV файл пуст или не содержит данных")
            sys.exit(1)
        
        # Создаем бота
        bot = Bot(token=BOT_TOKEN)
        
        # Запускаем воронку с поддержкой вариантов
        await send_funnel(bot, users_df, output_dir, send_real, args.variant)
        
    except FileNotFoundError as e:
        print(f"❌ Ошибка: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
        sys.exit(1)
    finally:
        # Закрываем сессию бота
        if 'bot' in locals():
            await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️  Программа остановлена пользователем")
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        sys.exit(1)
