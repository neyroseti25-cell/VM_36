import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Токен бота из переменных окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Этапы воронки
STAGES = ['interest', 'solution', 'deadline']

# Варианты для A/B-тестирования
VARIANTS = ['a', 'b', 'c']

# Брендинг Poznay Sebya
BRAND = {
    'logo': 'POZNAY SEBYA / KNOW YOURSELF',
    'colors': {
        'bg': '#F5F3EF',        # natural harmony
        'text': '#4A4F46',      # soul
        'accent': '#A38DA2',    # mindful
        'highlight': '#8CA29B', # authenticity
        'warm': '#E3D6C4'       # subtle gradient
    }
}

# Шрифты
FONTS = {
    'heading': 'Cormorant Garamond, serif',
    'body': 'Inter, sans-serif'
}

# Базовый URL для кнопок
BASE_URL = 'https://poznaysebya.com'

# Настройки изображений
IMAGE_WIDTH = 800
IMAGE_HEIGHT = 600

# Задержка между отправкой сообщений (секунды)
SEND_DELAY = 1
