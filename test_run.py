"""
Быстрый запуск всех тестов
Запускает тесты моделей и API с выводом результатов
"""

import subprocess
import sys
import os


def print_header(text):
    """Вывод заголовка"""
    print("=" * 60)
    print(f"     {text}")
    print("=" * 60)


def run_test(test_file):
    """Запуск тестового файла"""
    print(f"\n📋 Запуск {test_file}...")
    print("-" * 60)
    
    result = subprocess.run(
        [sys.executable, test_file],
        cwd="server",
        capture_output=False,
        text=True
    )
    
    if result.returncode == 0:
        print(f"\n✅ {test_file} ПРОЙДЕН!")
    else:
        print(f"\n❌ {test_file} НЕ ПРОЙДЕН!")
    
    return result.returncode == 0


def main():
    """Главная функция"""
    print_header("ЗАПУСК ВСЕХ ТЕСТОВ")
    
    # Проверяем, что мы в правильной папке
    if not os.path.exists("server"):
        print("❌ Ошибка: папка 'server' не найдена!")
        print("   Запустите скрипт из корневой папки проекта.")
        return
    
    # Запускаем тесты
    tests = [
        ("test_models.py", "Тесты моделей"),
        ("test_api.py", "Тесты API")
    ]
    
    all_passed = True
    
    for test_file, test_name in tests:
        print(f"\n{'=' * 60}")
        print(f"     {test_name}")
        print(f"{'=' * 60}")
        
        result = subprocess.run(
            [sys.executable, test_file],
            cwd="server",
            capture_output=False,
            text=True
        )
        
        if result.returncode != 0:
            all_passed = False
    
    # Итоговый результат
    print("\n" + "=" * 60)
    if all_passed:
        print("     ✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
    else:
        print("     ❌ НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОЙДЕНЫ!")
    print("=" * 60)


if __name__ == "__main__":
    main()