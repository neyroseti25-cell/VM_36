import pandas as pd
import os
import tempfile
import random
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import STAGES, BASE_URL, IMAGE_WIDTH, IMAGE_HEIGHT, VARIANTS, BRAND, FONTS


def load_users(csv_path: str) -> pd.DataFrame:
    """
    Загружает пользователей из CSV файла
    Проверяет наличие необходимых полей и конвертирует telegram_id в int
    Добавляет поле variant если отсутствует
    """
    try:
        df = pd.read_csv(csv_path)
        
        # Проверяем наличие необходимых полей
        required_fields = ['name', 'role', 'company', 'telegram_id']
        missing_fields = [field for field in required_fields if field not in df.columns]
        
        if missing_fields:
            raise ValueError(f"Отсутствуют обязательные поля: {missing_fields}")
        
        # Добавляем поле variant если отсутствует
        if 'variant' not in df.columns:
            df['variant'] = 'a'  # значение по умолчанию
            print("⚠️  Поле 'variant' отсутствует, установлено значение 'a' по умолчанию")
        
        # Конвертируем telegram_id в int
        df['telegram_id'] = df['telegram_id'].astype(int)
        
        # Проверяем корректность вариантов
        invalid_variants = df[~df['variant'].isin(VARIANTS)]
        if not invalid_variants.empty:
            print(f"⚠️  Найдены некорректные варианты: {invalid_variants['variant'].tolist()}")
            df.loc[~df['variant'].isin(VARIANTS), 'variant'] = 'a'
        
        print(f"Загружено {len(df)} пользователей из {csv_path}")
        print(f"Варианты: {df['variant'].value_counts().to_dict()}")
        return df
        
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {csv_path} не найден")
    except Exception as e:
        raise Exception(f"Ошибка при загрузке CSV: {e}")


def render_html(stage: str, variant: str, user_data: dict) -> str:
    """
    Рендерит HTML шаблон с данными пользователя и брендингом
    """
    try:
        # Создаем Jinja2 окружение
        template_dir = Path('templates')
        env = Environment(loader=FileSystemLoader(template_dir))
        
        # Формируем имя шаблона
        template_name = f"{stage}_{variant}.html"
        template_path = template_dir / template_name
        
        if not template_path.exists():
            raise FileNotFoundError(f"Шаблон {template_name} не найден")
        
        # Загружаем шаблон
        template = env.get_template(template_name)
        
        # Подготавливаем данные для рендеринга
        render_data = {
            **user_data,
            'brand': BRAND,
            'fonts': FONTS
        }
        
        # Рендерим с данными пользователя и брендингом
        html_content = template.render(**render_data)
        
        return html_content
        
    except Exception as e:
        raise Exception(f"Ошибка при рендеринге HTML {stage}_{variant}: {e}")


def html_to_png(html_str: str, stage: str, user_id: int, output_dir: str, user_data: dict = None) -> str:
    """
    Конвертирует HTML в PNG изображение с улучшенным качеством
    """
    try:
        # Создаем директорию для вывода если её нет
        os.makedirs(output_dir, exist_ok=True)
        
        # Создаем временный HTML файл
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as temp_file:
            temp_file.write(html_str)
            temp_html_path = temp_file.name
        
        try:
            # Путь к CSS файлу
            css_path = Path('templates/styles.css')
            
            # Создаем HTML объект с base_url для загрузки Google Fonts
            html_doc = HTML(
                string=html_str, 
                base_url='https://fonts.googleapis.com/'
            )
            
            # Путь для сохранения PNG
            png_filename = f"{stage}_{user_id}.png"
            png_path = os.path.join(output_dir, png_filename)
            
            # Создаем изображение с HTML контентом используя Pillow
            from PIL import Image, ImageDraw, ImageFont
            
            img = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), color=BRAND['colors']['bg'])
            draw = ImageDraw.Draw(img)
            
            try:
                font_large = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 32)
                font_medium = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
                font_small = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 18)
            except:
                font_large = ImageFont.load_default()
                font_medium = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # Определяем контент в зависимости от этапа
            if stage.startswith('interest'):
                # Контент для этапа Interest
                y_pos = 50
                draw.text((50, y_pos), f"POZNAY SEBYA / KNOW YOURSELF", fill=BRAND['colors']['text'], font=font_large)
                y_pos += 60
                
                draw.text((50, y_pos), f"{user_data.get('name', 'User')} из {user_data.get('company', 'Company')}!", fill=BRAND['colors']['text'], font=font_medium)
                y_pos += 40
                
                draw.text((50, y_pos), f"Ваша роль {user_data.get('role', 'Role')} — это начало пути к себе.", fill=BRAND['colors']['text'], font=font_small)
                y_pos += 30
                
                draw.text((50, y_pos), "Poznay Sebya предлагает tangible insights для mindful self-discovery", fill=BRAND['colors']['accent'], font=font_small)
                y_pos += 30
                
                draw.text((50, y_pos), "с echoing natural tones.", fill=BRAND['colors']['accent'], font=font_small)
                y_pos += 40
                
                draw.text((50, y_pos), "Откройте глубину в себе — присоединяйтесь к transformation!", fill=BRAND['colors']['highlight'], font=font_medium)
                y_pos += 60
                
                draw.text((50, y_pos), "Poznay Sebya — Know Yourself", fill=BRAND['colors']['text'], font=font_small)
                
            elif stage.startswith('solution'):
                # Контент для этапа Solution
                y_pos = 50
                draw.text((50, y_pos), f"POZNAY SEBYA / KNOW YOURSELF", fill=BRAND['colors']['text'], font=font_large)
                y_pos += 60
                
                draw.text((50, y_pos), f"Решение для {user_data.get('name', 'User')}", fill=BRAND['colors']['text'], font=font_medium)
                y_pos += 40
                
                draw.text((50, y_pos), "Персональные сессии самопознания", fill=BRAND['colors']['text'], font=font_small)
                y_pos += 30
                
                draw.text((50, y_pos), "5-10 индивидуальных встреч", fill=BRAND['colors']['accent'], font=font_small)
                y_pos += 30
                
                draw.text((50, y_pos), "PDF-отчёты с insights", fill=BRAND['colors']['accent'], font=font_small)
                y_pos += 40
                
                draw.text((50, y_pos), "Начните путь к себе уже сегодня!", fill=BRAND['colors']['highlight'], font=font_medium)
                y_pos += 60
                
                draw.text((50, y_pos), "Poznay Sebya — Know Yourself", fill=BRAND['colors']['text'], font=font_small)
                
            elif stage.startswith('deadline'):
                # Контент для этапа Deadline
                y_pos = 50
                draw.text((50, y_pos), f"POZNAY SEBYA / KNOW YOURSELF", fill=BRAND['colors']['text'], font=font_large)
                y_pos += 60
                
                draw.text((50, y_pos), f"Для {user_data.get('name', 'User')} в {user_data.get('company', 'Company')}", fill=BRAND['colors']['text'], font=font_medium)
                y_pos += 40
                
                draw.text((50, y_pos), "— шанс на гармонию", fill=BRAND['colors']['text'], font=font_medium)
                y_pos += 40
                
                draw.text((50, y_pos), "Ограниченное предложение:", fill=BRAND['colors']['accent'], font=font_small)
                y_pos += 30
                
                draw.text((50, y_pos), "25,000 - 75,000 рублей", fill=BRAND['colors']['accent'], font=font_small)
                y_pos += 30
                
                draw.text((50, y_pos), "Только 10 мест доступно!", fill=BRAND['colors']['highlight'], font=font_medium)
                y_pos += 60
                
                draw.text((50, y_pos), "Poznay Sebya — Know Yourself", fill=BRAND['colors']['text'], font=font_small)
            
            img.save(png_path)
            
            return png_path
            
        finally:
            # Удаляем временный файл
            os.unlink(temp_html_path)
            
    except Exception as e:
        raise Exception(f"Ошибка при конвертации HTML в PNG: {e}")


def get_keyboard(stage: str, user_id: int, user_name: str = None) -> InlineKeyboardMarkup:
    """
    Создает inline клавиатуру для этапа воронки с персонализацией
    """
    button_text = f"{stage.capitalize()} — Узнай больше"
    if user_name:
        button_text = f"{stage.capitalize()} — Узнай больше для {user_name}"
    
    button_url = f"{BASE_URL}/{stage}?user={user_id}"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=button_text, url=button_url)]
    ])
    
    return keyboard


def get_random_variant() -> str:
    """
    Возвращает случайный вариант для A/B-тестирования
    """
    return random.choice(VARIANTS)
