@echo off
echo ============================================================
echo     СИСТЕМА ТЕХНИЧЕСКОЙ ПОДДЕРЖКИ
echo ============================================================
echo.
echo Запуск сервера и клиента...
echo.

REM Активируем виртуальное окружение
call venv\Scripts\activate

REM Запускаем сервер в новом окне
start "Сервер Tech Support" cmd /k "cd server && python app.py"

REM Ждём 3 секунды
timeout /t 3 /nobreak >nul

REM Запускаем клиент в новом окне
start "Клиент Tech Support" cmd /k "cd client && python client.py"

echo.
echo ✅ Приложение запущено!
echo.
echo    - Сервер работает в отдельном окне
echo    - Клиент работает в отдельном окне
echo.
echo ⚠️ Для остановки закройте окна терминала
echo.
pause