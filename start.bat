@echo off
chcp 65001 >nul
title Система технической поддержки

echo ============================================================
echo     СИСТЕМА ТЕХНИЧЕСКОЙ ПОДДЕРЖКИ
echo ============================================================
echo.

echo [1/6] Проверка наличия Python...
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
echo [2/6] Проверка виртуального окружения...
if not exist venv (
    echo Создание виртуального окружения...
    python -m venv venv
)
echo ✅ Виртуальное окружение готово

echo.
echo [3/6] Активация виртуального окружения...
call venv\Scripts\activate
echo ✅ Виртуальное окружение активировано

echo.
echo [4/6] Проверка и установка зависимостей...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo Установка зависимостей...
    pip install Flask flask-cors requests
    echo ✅ Зависимости установлены
) else (
    echo ✅ Зависимости уже установлены
)

echo.
echo [5/6] Запуск тестов...
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
echo [6/6] Запуск приложения...
echo.

REM Запускаем сервер в новом окне
start "Сервер Tech Support" cmd /k "cd server && python app.py"

REM Ждём 3 секунды
timeout /t 3 /nobreak >nul

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
echo    Результаты тестов показаны выше
echo.
echo    Для остановки закройте окна терминалов
echo.
pause