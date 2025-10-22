#!/usr/bin/env python3
"""
Тестовый скрипт для проверки работы системы воронки
"""

import os
import sys
from pathlib import Path

# Добавляем текущую директорию в путь для импорта
sys.path.append('.')

from utils import load_users, render_html, html_to_png
from config import STAGES


def test_csv_loading():
    """Тестирует загрузку CSV файла"""
    print("🧪 Тестируем загрузку CSV...")
    try:
        df = load_users('users.csv')
        print(f"✅ CSV загружен успешно: {len(df)} пользователей")
        print(f"Поля: {list(df.columns)}")
        return df
    except Exception as e:
        print(f"❌ Ошибка загрузки CSV: {e}")
        return None


def test_html_rendering():
    """Тестирует рендеринг HTML шаблонов"""
    print("\n🧪 Тестируем рендеринг HTML...")
    
    test_user = {
        'name': 'Test User',
        'role': 'Test Role',
        'company': 'Test Company'
    }
    
    for stage in STAGES:
        try:
            template_path = f"templates/{stage}.html"
            html = render_html(template_path, test_user)
            print(f"✅ {stage}.html рендерится успешно")
        except Exception as e:
            print(f"❌ Ошибка рендеринга {stage}.html: {e}")


def test_png_generation():
    """Тестирует генерацию PNG"""
    print("\n🧪 Тестируем генерацию PNG...")
    
    test_user = {
        'name': 'Test User',
        'role': 'Test Role', 
        'company': 'Test Company'
    }
    
    # Создаем директорию для тестов
    test_output = "test_output"
    os.makedirs(test_output, exist_ok=True)
    
    for stage in STAGES:
        try:
            template_path = f"templates/{stage}.html"
            html = render_html(template_path, test_user)
            png_path = html_to_png(html, stage, 999999, test_output)
            print(f"✅ {stage}.png создан: {png_path}")
        except Exception as e:
            print(f"❌ Ошибка создания {stage}.png: {e}")


def main():
    """Основная функция тестирования"""
    print("🚀 Запуск тестирования системы воронки\n")
    
    # Проверяем наличие файлов
    required_files = [
        'users.csv',
        'templates/interest.html',
        'templates/solution.html', 
        'templates/deadline.html',
        'templates/styles.css'
    ]
    
    print("📁 Проверяем наличие файлов...")
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - файл не найден")
            return
    
    # Запускаем тесты
    df = test_csv_loading()
    if df is not None:
        test_html_rendering()
        test_png_generation()
    
    print("\n🎉 Тестирование завершено!")
    print("Для полного теста запустите: python bot_funnel.py --test")


if __name__ == "__main__":
    main()

