@echo off
chcp 65001 >nul
title Система технической поддержки

echo ============================================================
echo     СИСТЕМА ТЕХНИЧЕСКОЙ ПОДДЕРЖКИ
echo ============================================================
echo.

echo [1/8] Проверка наличия Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не найден!
    echo.
    echo Скачайте и установите Python с сайта: https://www.python.org/downloads/
    echo.
    echo ⚠️ При установке ОБЯЗАТЕЛЬНО отметьте галочку "Add Python to PATH"
    echo.
    pause
    exit /b
)
echo ✅ Python найден

echo.
echo [2/8] Проверка виртуального окружения...
if not exist venv (
    echo Создание виртуального окружения...
    python -m venv venv
)
echo ✅ Виртуальное окружение готово

echo.
echo [3/8] Активация виртуального окружения...
call venv\Scripts\activate
echo ✅ Виртуальное окружение активировано

echo.
echo [4/8] Проверка и установка зависимостей...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo Установка зависимостей...
    pip install Flask flask-cors requests
    echo ✅ Зависимости установлены
) else (
    echo ✅ Зависимости уже установлены
)

echo.
echo [5/8] Запуск тестов...
echo.
echo ============================================================
echo     ЗАПУСК ТЕСТОВ
echo ============================================================
echo.
cd server

echo --- Тесты моделей (test_models.py) ---
python test_models.py
if errorlevel 1 (
    echo ❌ Тесты моделей НЕ ПРОЙДЕНЫ!
) else (
    echo ✅ Тесты моделей ПРОЙДЕНЫ!
)
echo.

echo --- Тесты API (test_api.py) ---
python test_api.py
if errorlevel 1 (
    echo ❌ Тесты API НЕ ПРОЙДЕНЫ!
) else (
    echo ✅ Тесты API ПРОЙДЕНЫ!
)
echo.

cd ..
echo ============================================================
echo.

echo.
echo [6/8] Запуск сервера...
echo.

REM Запускаем сервер в новом окне
start "Сервер Tech Support" cmd /k "cd server && python app.py"

REM Ждём 5 секунд для полного запуска сервера
echo ⏳ Ожидание запуска сервера (5 секунд)...
timeout /t 5 /nobreak >nul

echo.
echo [7/8] Проверка и заполнение базы данных...
echo.

REM Проверяем, существует ли файл БД и есть ли в нём данные
set DB_EMPTY=1
if exist server\tech_support.db (
    python -c "import sqlite3; conn = sqlite3.connect('server/tech_support.db'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM questions'); count = cursor.fetchone()[0]; conn.close(); exit(0 if count > 0 else 1)" >nul 2>&1
    if not errorlevel 1 (
        set DB_EMPTY=0
    )
)

if %DB_EMPTY%==1 (
    echo 📋 База данных пуста или отсутствует. Заполнение тестовыми данными...
    python seed.py
    echo ✅ Заполнение завершено!
) else (
    echo ✅ База данных уже содержит данные
)

echo.
echo [8/8] Запуск клиента...
echo.

REM Запускаем клиент в новом окне
start "Клиент Tech Support" cmd /k "cd client && python client.py"

echo.
echo ============================================================
echo ✅ Приложение запущено!
echo ============================================================
echo.
echo    Сервер: http://localhost:5000
echo    Клиент: Открыто отдельное окно
echo.
echo    База данных заполнена тестовыми данными!
echo    В меню будут отображаться вопросы и консультанты.
echo.
echo    Результаты тестов показаны выше
echo.
echo    Для остановки закройте окна терминалов
echo.
pause