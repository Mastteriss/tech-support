# 🖥️ Система технической поддержки

> Клиент-серверное приложение для автоматизации работы службы технической поддержки

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.2-green.svg)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3-important.svg)](https://www.sqlite.org/)

---

## 📋 Описание проекта

**Система технической поддержки** — это клиент-серверное приложение для управления вопросами клиентов в службе технической поддержки.

### Основные функции:
- ✅ Регистрация и обработка вопросов клиентов
- ✅ Назначение консультантов на вопросы
- ✅ Добавление ответов и ведение истории
- ✅ Отслеживание статуса каждого вопроса
- ✅ Статистика работы службы поддержки

---

## 📥 Что нужно скачать и установить

### 1. Python (обязательно)

Скачайте и установите Python версии 3.8 или выше:

| ОС | Ссылка для скачивания |
|----|----------------------|
| **Windows** | [python.org/downloads/windows/](https://www.python.org/downloads/windows/) |
| **macOS** | [python.org/downloads/mac-osx/](https://www.python.org/downloads/mac-osx/) |
| **Linux** | `sudo apt install python3 python3-pip` |

> ⚠️ **Важно для Windows:** при установке обязательно отметьте галочку **"Add Python to PATH"**

#### Проверка установки:
```bash
python --version
# Должно показать: Python 3.8 или выше
```

---

### 2. Git (для скачивания через терминал)

| ОС | Ссылка для скачивания |
|----|----------------------|
| **Windows** | [git-scm.com/download/win](https://git-scm.com/download/win) |
| **macOS** | [git-scm.com/download/mac](https://git-scm.com/download/mac) |
| **Linux** | `sudo apt install git` |

#### Проверка установки:
```bash
git --version
# Должно показать: git version 2.x.x
```

---

### 3. VS Code (рекомендуется)

| ОС | Ссылка для скачивания |
|----|----------------------|
| **Windows** | [code.visualstudio.com/download](https://code.visualstudio.com/download) |
| **macOS** | [code.visualstudio.com/download](https://code.visualstudio.com/download) |
| **Linux** | [code.visualstudio.com/download](https://code.visualstudio.com/download) |

#### Расширения для VS Code (рекомендуемые):
- **Python** (от Microsoft) — для работы с Python
- **Mermaid Preview** — для просмотра диаграмм

---

## 📦 Что докачивать не нужно (уже в проекте)

| Компонент | Где находится | Описание |
|-----------|---------------|----------|
| **Код сервера** | `server/` | Flask приложение с REST API |
| **Код клиента** | `client/` | GUI приложение на Tkinter |
| **Документация** | `docs/` | 8 документов по ГОСТ 19 |
| **Зависимости** | `requirements.txt` | Список библиотек для установки |
| **Тесты** | `server/test_*.py` | Модульные тесты |

---

## 🚀 Установка и запуск

### Шаг 1: Скачайте проект

#### Способ 1: Через Git (рекомендуется)
```bash
git clone https://github.com/Mastteriss/tech-support.git
cd tech-support
```

#### Способ 2: Скачать ZIP-архив
1. Перейдите на: https://github.com/Mastteriss/tech-support
2. Нажмите **"Code"** → **"Download ZIP"**
3. Распакуйте архив в удобное место

---

### Шаг 2: Установите зависимости

#### Создайте виртуальное окружение:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

#### Установите библиотеки:
```bash
pip install -r requirements.txt
```

#### Что установится:
| Библиотека | Версия | Для чего |
|------------|--------|----------|
| Flask | 2.3.2 | Веб-сервер |
| flask-cors | 4.0.0 | Поддержка CORS |
| requests | 2.31.0 | HTTP клиент |

---

### Шаг 3: Запустите приложение

#### Запуск сервера (Терминал 1):
```bash
cd server
python app.py
```

**Ожидаемый вывод:**
```
* Serving Flask app 'app'
* Debug mode: on
* Running on http://127.0.0.1:5000
```

> ⚠️ **Не закрывайте этот терминал!** Сервер должен работать постоянно.

#### Запуск клиента (Терминал 2):
```bash
cd client
python client.py
```

**Откроется окно приложения!** 🎉

---

## 🔧 Быстрый запуск (для Windows)

Создайте файл `start.bat` в корневой папке проекта:

```batch
@echo off
chcp 65001 >nul
echo ==================================================
echo     СИСТЕМА ТЕХНИЧЕСКОЙ ПОДДЕРЖКИ
echo ==================================================
echo.

call venv\Scripts\activate

start "Сервер Tech Support" cmd /k "cd /d %~dp0server && python app.py"

timeout /t 3 /nobreak >nul

start "Клиент Tech Support" cmd /k "cd /d %~dp0client && python client.py"

echo.
echo ✅ Приложение запущено!
echo.
echo    Сервер: http://localhost:5000
echo    Клиент: Открыто отдельное окно
echo.
echo ⚠️ Для остановки закройте окна терминалов
echo.
pause
```

Теперь достаточно **дважды кликнуть** на `start.bat`.

---

## 🐧 Быстрый запуск (для macOS / Linux)

Создайте файл `start.sh`:

```bash
#!/bin/bash
echo "=================================================="
echo "     СИСТЕМА ТЕХНИЧЕСКОЙ ПОДДЕРЖКИ"
echo "=================================================="
echo ""

source venv/bin/activate

if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    osascript -e 'tell app "Terminal" to do script "cd '$PWD'/server && python app.py"'
    sleep 3
    osascript -e 'tell app "Terminal" to do script "cd '$PWD'/client && python client.py"'
else
    # Linux
    gnome-terminal -- bash -c "cd server && python app.py; exec bash" &
    sleep 3
    gnome-terminal -- bash -c "cd client && python client.py; exec bash" &
fi

echo ""
echo "✅ Приложение запущено!"
echo ""
```

Дайте права на выполнение:
```bash
chmod +x start.sh
./start.sh
```

---

## 🧪 Запуск тестов

```bash
cd server

# Тесты моделей (16 тестов)
python test_models.py

# Тесты API (8 тестов)
python test_api.py

# Все тесты вместе
python -m unittest discover
```

**Ожидаемый результат:** ✅ Все 24 теста пройдены

---

## ❓ Частые проблемы и решения

### 1. "python не найден"
**Причина:** Python не установлен или не в PATH.  
**Решение:** Скачайте Python с https://python.org/ и при установке отметьте **"Add Python to PATH"**

### 2. "ModuleNotFoundError: No module named 'flask'"
**Причина:** Библиотеки не установлены.  
**Решение:** `pip install Flask flask-cors requests`

### 3. "Port 5000 already in use"
**Причина:** Порт занят другим приложением.  
**Решение:** Измените порт в `server/app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### 4. "Tkinter не установлен"
**Windows:** Tkinter обычно уже установлен.  
**macOS:** `brew install python-tk`  
**Linux:** `sudo apt-get install python3-tk`

### 5. "Permission denied" при запуске
**Решение:** `chmod +x start.sh`

---

## ✅ Проверка работоспособности

### Проверка сервера:
Откройте браузер и перейдите:
```
http://localhost:5000/api/health
```
Должен появиться ответ:
```json
{"status":"ok","message":"Tech Support API is running"}
```

### Проверка клиента:
После запуска должно открыться окно с тремя вкладками:
1. 📋 Вопросы
2. 👤 Консультанты
3. 📊 Статистика

---

## 📁 Структура проекта

```
tech-support/
├── server/                      # Серверная часть
│   ├── app.py                  # Flask приложение (REST API)
│   ├── models.py               # Модели данных (ООП)
│   ├── database.py             # Работа с SQLite
│   ├── test_models.py          # Модульные тесты (16 тестов)
│   └── test_api.py             # Тесты API (8 тестов)
├── client/                      # Клиентская часть
│   └── client.py               # GUI на Tkinter
├── docs/                        # Документация по ГОСТ 19
│   ├── 12_техническое_задание.txt
│   ├── 13_программа_методика_испытаний.txt
│   ├── 31_руководство_программиста.txt
│   ├── 32_руководство_оператора.txt
│   ├── 33_руководство_пользователя.txt
│   ├── 34_спецификация.txt
│   ├── 51_описание_применения.txt
│   └── 81_пояснительная_записка.txt
├── venv/                        # Виртуальное окружение
├── requirements.txt             # Зависимости
├── README.md                    # Описание проекта
├── start.bat                    # Быстрый запуск (Windows)
└── start.sh                     # Быстрый запуск (macOS/Linux)
```

---

## 👥 Автор

**Иванов Иван Иванович**
- Группа: ИС-202
- GitHub: [@Mastteriss](https://github.com/Mastteriss)

---

**© 2024 - Система технической поддержки**
