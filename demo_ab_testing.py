#!/usr/bin/env python3
"""
Демонстрация A/B-тестирования воронки анонсов
"""

import os
import sys
from pathlib import Path

# Добавляем текущую директорию в путь для импорта
sys.path.append('.')

def demo_variants():
    """Демонстрирует различные варианты шаблонов"""
    print("🎯 Демонстрация A/B-тестирования воронки анонсов\n")
    
    # Проверяем наличие всех шаблонов
    stages = ['interest', 'solution', 'deadline']
    variants = ['a', 'b', 'c']
    
    print("📋 Проверяем наличие всех шаблонов:")
    all_templates_exist = True
    
    for stage in stages:
        for variant in variants:
            template_path = f"templates/{stage}_{variant}.html"
            if Path(template_path).exists():
                print(f"✅ {template_path}")
            else:
                print(f"❌ {template_path} - отсутствует")
                all_templates_exist = False
    
    if not all_templates_exist:
        print("\n❌ Не все шаблоны найдены. Создайте недостающие файлы.")
        return False
    
    print(f"\n🎨 Всего шаблонов: {len(stages) * len(variants)}")
    print("   Этапы:", ', '.join(stages))
    print("   Варианты:", ', '.join(variants))
    
    return True


def demo_csv_variants():
    """Демонстрирует варианты в CSV файле"""
    print("\n📊 Анализ вариантов в CSV файле:")
    
    try:
        with open('users.csv', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if len(lines) < 2:
            print("❌ CSV файл пуст")
            return False
        
        # Анализируем варианты
        variants = []
        for line in lines[1:]:
            parts = line.strip().split(',')
            if len(parts) >= 5:
                variants.append(parts[4])
        
        variant_counts = {}
        for variant in variants:
            variant_counts[variant] = variant_counts.get(variant, 0) + 1
        
        print("   Распределение вариантов:")
        for variant, count in variant_counts.items():
            percentage = (count / len(variants)) * 100
            print(f"   - Вариант {variant.upper()}: {count} пользователей ({percentage:.1f}%)")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка анализа CSV: {e}")
        return False


def demo_branding():
    """Демонстрирует брендинг Poznay Sebya"""
    print("\n🎨 Брендинг Poznay Sebya:")
    
    try:
        from config import BRAND, FONTS
        
        print("   Логотип:", BRAND['logo'])
        print("   Цвета:")
        for color_name, color_value in BRAND['colors'].items():
            print(f"   - {color_name}: {color_value}")
        
        print("   Шрифты:")
        for font_type, font_value in FONTS.items():
            print(f"   - {font_type}: {font_value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка загрузки брендинга: {e}")
        return False


def demo_usage_examples():
    """Показывает примеры использования"""
    print("\n🚀 Примеры использования:")
    
    print("\n1. Тестирование с фиксированными вариантами:")
    print("   python3 bot_funnel.py --test")
    print("   # Использует варианты из CSV файла")
    
    print("\n2. Тестирование со случайными вариантами:")
    print("   python3 bot_funnel.py --test --variant random")
    print("   # Случайно выбирает a, b или c для каждого пользователя")
    
    print("\n3. Отправка с фиксированными вариантами:")
    print("   python3 bot_funnel.py --send")
    print("   # Отправляет сообщения с вариантами из CSV")
    
    print("\n4. Отправка со случайными вариантами:")
    print("   python3 bot_funnel.py --send --variant random")
    print("   # Отправляет сообщения со случайными вариантами")
    
    print("\n5. Проверка системы:")
    print("   python3 test_basic.py")
    print("   # Проверяет все компоненты системы")


def demo_expected_output():
    """Показывает ожидаемый результат"""
    print("\n📈 Ожидаемый результат:")
    
    print("   При запуске --test будет создано:")
    print("   - 5 пользователей × 3 этапа × 1 вариант = 15 PNG файлов")
    print("   - Файлы: interest_a_123456789.png, solution_b_987654321.png, etc.")
    
    print("\n   При запуске --variant random:")
    print("   - Каждый пользователь получит случайный вариант для каждого этапа")
    print("   - Статистика покажет распределение: {'a': 5, 'b': 6, 'c': 4}")
    
    print("\n   Структура PNG файлов:")
    print("   - Размер: 800x600 пикселей")
    print("   - Брендинг: Poznay Sebya с фирменными цветами")
    print("   - Шрифты: Cormorant Garamond + Inter")
    print("   - Содержание: персонализированные сообщения для каждого пользователя")


def main():
    """Основная функция демонстрации"""
    print("🎯 Демонстрация A/B-тестирования воронки анонсов Poznay Sebya\n")
    
    # Проверяем компоненты
    checks = [
        demo_variants(),
        demo_csv_variants(),
        demo_branding()
    ]
    
    if all(checks):
        print("\n✅ Все компоненты готовы!")
        
        # Показываем примеры использования
        demo_usage_examples()
        demo_expected_output()
        
        print("\n" + "="*60)
        print("🎉 Система готова к A/B-тестированию!")
        print("Запустите: python3 bot_funnel.py --test --variant random")
        
    else:
        print("\n❌ Некоторые компоненты не готовы. Исправьте ошибки.")


if __name__ == "__main__":
    main()

