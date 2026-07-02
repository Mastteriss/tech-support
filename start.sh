#!/bin/bash

# Скрипт запуска системы технической поддержки
# с автоматической проверкой и установкой зависимостей

echo "============================================================"
echo "     СИСТЕМА ТЕХНИЧЕСКОЙ ПОДДЕРЖКИ"
echo "============================================================"
echo ""

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "[1/5] Проверка наличия Python..."
if command -v python3 &>/dev/null; then
    echo -e "${GREEN}✅ Python найден${NC}"
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    echo -e "${GREEN}✅ Python найден${NC}"
    PYTHON_CMD="python"
else
    echo -e "${RED}❌ Python не найден!${NC}"
    echo ""
    echo "Скачайте и установите Python с сайта: https://www.python.org/downloads/"
    echo ""
    exit 1
fi

echo ""
echo "[2/5] Проверка виртуального окружения..."
if [ ! -d "venv" ]; then
    echo "Создание виртуального окружения..."
    $PYTHON_CMD -m venv venv
fi
echo -e "${GREEN}✅ Виртуальное окружение готово${NC}"

echo ""
echo "[3/5] Активация виртуального окружения..."
source venv/bin/activate
echo -e "${GREEN}✅ Виртуальное окружение активировано${NC}"

echo ""
echo "[4/5] Проверка и установка зависимостей..."
if ! pip show flask &>/dev/null; then
    echo "Установка зависимостей..."
    pip install Flask flask-cors requests
    echo -e "${GREEN}✅ Зависимости установлены${NC}"
else
    echo -e "${GREEN}✅ Зависимости уже установлены${NC}"
fi

echo ""
echo "[5/5] Запуск приложения..."
echo ""

# Определяем ОС и запускаем
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # Windows (Git Bash / Cygwin)
    start "Сервер Tech Support" cmd /k "cd server && python app.py"
    sleep 3
    start "Клиент Tech Support" cmd /k "cd client && python client.py"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    osascript -e "tell app \"Terminal\" to do script \"cd '$PWD'/server && python app.py\""
    sleep 3
    osascript -e "tell app \"Terminal\" to do script \"cd '$PWD'/client && python client.py\""
else
    # Linux
    if command -v gnome-terminal &>/dev/null; then
        gnome-terminal -- bash -c "cd server && python app.py; exec bash" &
        sleep 3
        gnome-terminal -- bash -c "cd client && python client.py; exec bash" &
    elif command -v xterm &>/dev/null; then
        xterm -e "cd server && python app.py" &
        sleep 3
        xterm -e "cd client && python client.py" &
    else
        echo -e "${YELLOW}⚠️ Не найден терминал. Запускаем в текущем окне...${NC}"
        python server/app.py &
        sleep 3
        python client/client.py &
    fi
fi

echo ""
echo "============================================================"
echo -e "${GREEN}✅ Приложение запущено!${NC}"
echo "============================================================"
echo ""
echo "   Сервер: http://localhost:5000"
echo "   Клиент: Открыто отдельное окно"
echo ""
echo "   Для остановки закройте окна терминалов"
echo ""