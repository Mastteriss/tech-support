#!/bin/bash

# Скрипт запуска системы технической поддержки

echo "============================================================"
echo "     СИСТЕМА ТЕХНИЧЕСКОЙ ПОДДЕРЖКИ"
echo "============================================================"
echo ""

# Активируем виртуальное окружение
echo "Активация виртуального окружения..."
source venv/bin/activate

# Запускаем сервер в новом терминале
echo "Запуск сервера..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    osascript -e 'tell app "Terminal" to do script "cd '$PWD'/server && python app.py"'
else
    # Linux
    gnome-terminal -- bash -c "cd server && python app.py; exec bash" &
fi

# Ждём 3 секунды
sleep 3

# Запускаем клиент в новом терминале
echo "Запуск клиента..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    osascript -e 'tell app "Terminal" to do script "cd '$PWD'/client && python client.py"'
else
    # Linux
    gnome-terminal -- bash -c "cd client && python client.py; exec bash" &
fi

echo ""
echo "✅ Приложение запущено!"
echo ""
echo "   - Сервер работает в отдельном окне"
echo "   - Клиент работает в отдельном окне"
echo ""
echo "⚠️ Для остановки закройте окна терминала"
echo ""