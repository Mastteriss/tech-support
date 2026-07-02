"""
Единая точка запуска приложения "Система технической поддержки"
Запускает сервер и клиент одновременно в отдельных процессах
"""

import subprocess
import sys
import os
import time
import threading
import webbrowser
from pathlib import Path


def print_banner():
    """Вывод баннера приложения"""
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║     СИСТЕМА ТЕХНИЧЕСКОЙ ПОДДЕРЖКИ                            ║
║     Tech Support System v1.0                                 ║
║                                                               ║
║     Запуск сервера и клиента...                              ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def check_dependencies():
    """Проверка установленных зависимостей"""
    try:
        import flask
        import requests
        print("Все зависимости установлены")
        return True
    except ImportError as e:
        print(f"Ошибка: {e}")
        print("\nУстановите зависимости командой:")
        print("pip install Flask flask-cors requests")
        return False


def run_server():
    """Запуск сервера в отдельном процессе"""
    server_path = os.path.join(os.path.dirname(__file__), 'server', 'app.py')
    
    print("\n🚀 Запуск сервера...")
    print(f"   Файл: {server_path}")
    
    # Запускаем сервер
    process = subprocess.Popen(
        [sys.executable, server_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    # Читаем вывод сервера в реальном времени
    for line in process.stdout:
        print(f"[СЕРВЕР] {line.strip()}")
        if "Running on" in line:
            print("\nСервер успешно запущен!")
            print("   Адрес: http://localhost:5000")
            print("   API: http://localhost:5000/api/health")
    
    return process


def run_client():
    """Запуск клиента в отдельном процессе"""
    client_path = os.path.join(os.path.dirname(__file__), 'client', 'client.py')
    
    print("\n🖥️ Запуск клиента...")
    print(f"   Файл: {client_path}")
    
    # Запускаем клиент
    process = subprocess.Popen(
        [sys.executable, client_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    # Читаем вывод клиента в реальном времени
    for line in process.stdout:
        print(f"[КЛИЕНТ] {line.strip()}")
    
    return process


def open_browser():
    """Открывает браузер с проверкой API"""
    time.sleep(3)  # Ждём запуска сервера
    print("\nОткрываем браузер для проверки API...")
    webbrowser.open('http://localhost:5000/api/health')


def main():
    """Главная функция"""
    print_banner()
    
    # Проверяем зависимости
    if not check_dependencies():
        sys.exit(1)
    
    # Получаем путь к проекту
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    print(f"\n📁 Рабочая директория: {project_dir}")
    
    # Запускаем сервер в отдельном потоке
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Даём серверу время на запуск
    print("\n⏳ Ожидание запуска сервера (5 секунд)...")
    time.sleep(5)
    
    # Открываем браузер для проверки
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Запускаем клиент (основной поток)
    try:
        client_process = run_client()
    except KeyboardInterrupt:
        print("\n\n⏹Остановка приложения...")
    except Exception as e:
        print(f"\n❌ Ошибка при запуске клиента: {e}")
        print("   Проверьте, что файл client/client.py существует")
    
    print("\nПриложение завершено")


if __name__ == '__main__':
    main()