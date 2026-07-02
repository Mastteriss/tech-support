"""
Заполнение базы данных тестовыми данными
Для демонстрации работы приложения
"""

import requests
import time
import json


API_URL = 'http://localhost:5000/api'


def seed_data():
    """Заполнение БД тестовыми данными"""
    print("=" * 60)
    print("     ЗАПОЛНЕНИЕ ТЕСТОВЫМИ ДАННЫМИ")
    print("=" * 60)
    print()

    # Проверка, что сервер запущен
    try:
        response = requests.get(f'{API_URL}/health', timeout=2)
        if response.status_code != 200:
            print("❌ Сервер не запущен! Запустите сервер сначала.")
            return False
    except:
        print("❌ Сервер не запущен! Запустите сервер сначала.")
        return False

    print("✅ Сервер запущен, начинаем заполнение...")
    print()

    # 1. Создаем консультантов
    consultants = [
        {"name": "Иван Петров", "specialization": "Программное обеспечение", "email": "ivan@tech.com"},
        {"name": "Анна Смирнова", "specialization": "Веб-разработка", "email": "anna@tech.com"},
        {"name": "Сергей Козлов", "specialization": "Базы данных", "email": "sergey@tech.com"},
        {"name": "Елена Васильева", "specialization": "Сетевое оборудование", "email": "elena@tech.com"},
    ]

    created_consultants = []
    print("👤 Создание консультантов...")
    for c in consultants:
        try:
            response = requests.post(f'{API_URL}/consultants', json=c)
            if response.status_code == 201:
                data = response.json()
                created_consultants.append(data)
                print(f"   ✅ Создан: {c['name']} (ID: {data['id']})")
            else:
                print(f"   ❌ Ошибка создания {c['name']}: {response.text}")
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
    print()

    # 2. Создаем вопросы
    questions = [
        {
            "title": "Не работает главная страница сайта",
            "description": "После обновления сайта главная страница перестала загружаться. В консоли ошибка 404 на файл стилей. Срочно нужно исправить.",
            "client_name": "ООО 'ТехноСервис'",
            "priority": 3
        },
        {
            "title": "Ошибка при оформлении заказа",
            "description": "При оформлении заказа на последнем шаге вылетает ошибка 'Internal Server Error'. Клиенты не могут завершить покупку.",
            "client_name": "ООО 'Луч'",
            "priority": 3
        },
        {
            "title": "Не приходит письмо с подтверждением",
            "description": "После регистрации новым пользователям не приходит письмо с подтверждением. Проверили SMTP - вроде работает.",
            "client_name": "ИП 'Сидоров'",
            "priority": 2
        },
        {
            "title": "Медленная работа системы",
            "description": "В часы пик система работает очень медленно. Время ответа увеличилось с 2 до 15 секунд. Нужно оптимизировать запросы.",
            "client_name": "ЗАО 'Прогресс'",
            "priority": 2
        },
        {
            "title": "База данных не обновляется",
            "description": "После обновления через админку данные не сохраняются. В таблице обновления статус 'pending', но не применяется.",
            "client_name": "ООО 'Старт'",
            "priority": 1
        },
        {
            "title": "Проблема с авторизацией через Google",
            "description": "Пользователи не могут войти через Google OAuth. Выдает ошибку 'invalid_grant'. Ключи обновили, проблема осталась.",
            "client_name": "ООО 'Вектор'",
            "priority": 2
        },
    ]

    created_questions = []
    print("📋 Создание вопросов...")
    for q in questions:
        try:
            response = requests.post(f'{API_URL}/questions', json=q)
            if response.status_code == 201:
                data = response.json()
                created_questions.append(data)
                print(f"   ✅ Создан: {q['title'][:30]}... (ID: {data['id']})")
            else:
                print(f"   ❌ Ошибка создания: {response.text}")
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
    print()

    # 3. Назначаем консультантов и добавляем ответы
    if created_consultants and created_questions:
        print("👤 Назначение консультантов и добавление ответов...")

        # Назначаем первого консультанта на первый вопрос и добавляем ответ
        if len(created_questions) >= 1 and len(created_consultants) >= 1:
            q = created_questions[0]
            c = created_consultants[0]
            try:
                # Назначаем
                response = requests.put(
                    f'{API_URL}/questions/{q["id"]}/assign',
                    json={'consultant_id': c['id']}
                )
                if response.status_code == 200:
                    print(f"   ✅ Назначен {c['name']} на вопрос #{q['id']}")

                    # Добавляем ответ
                    answer = {
                        'question_id': q['id'],
                        'consultant_id': c['id'],
                        'content': 'Здравствуйте! Проверил ваш сайт. Проблема в файле index.html — неверный путь к CSS. Исправил, теперь всё работает. Проверьте, пожалуйста.'
                    }
                    response = requests.post(f'{API_URL}/answers', json=answer)
                    if response.status_code == 201:
                        print(f"   ✅ Добавлен ответ на вопрос #{q['id']}")
                        # Отмечаем как решенный
                        requests.put(f'{API_URL}/questions/{q["id"]}/resolve')
                        print(f"   ✅ Вопрос #{q['id']} отмечен как решенный")
                else:
                    print(f"   ❌ Ошибка назначения: {response.text}")
            except Exception as e:
                print(f"   ❌ Ошибка: {e}")

        # Назначаем второго консультанта на второй вопрос
        if len(created_questions) >= 2 and len(created_consultants) >= 2:
            q = created_questions[1]
            c = created_consultants[1]
            try:
                response = requests.put(
                    f'{API_URL}/questions/{q["id"]}/assign',
                    json={'consultant_id': c['id']}
                )
                if response.status_code == 200:
                    print(f"   ✅ Назначен {c['name']} на вопрос #{q['id']}")

                    # Добавляем ответ
                    answer = {
                        'question_id': q['id'],
                        'consultant_id': c['id'],
                        'content': 'Проверил логи заказа. Ошибка возникает из-за неверного формата данных в поле "phone". Исправляю, после тестов выкачу обновление.'
                    }
                    response = requests.post(f'{API_URL}/answers', json=answer)
                    if response.status_code == 201:
                        print(f"   ✅ Добавлен ответ на вопрос #{q['id']}")
                else:
                    print(f"   ❌ Ошибка назначения: {response.text}")
            except Exception as e:
                print(f"   ❌ Ошибка: {e}")

        # Назначаем третьего консультанта на третий вопрос
        if len(created_questions) >= 3 and len(created_consultants) >= 3:
            q = created_questions[2]
            c = created_consultants[2]
            try:
                response = requests.put(
                    f'{API_URL}/questions/{q["id"]}/assign',
                    json={'consultant_id': c['id']}
                )
                if response.status_code == 200:
                    print(f"   ✅ Назначен {c['name']} на вопрос #{q['id']}")
                else:
                    print(f"   ❌ Ошибка назначения: {response.text}")
            except Exception as e:
                print(f"   ❌ Ошибка: {e}")

    print()
    print("=" * 60)
    print("     ✅ ЗАПОЛНЕНИЕ ЗАВЕРШЕНО!")
    print("=" * 60)
    print()
    print(f"   ✅ Создано консультантов: {len(created_consultants)}")
    print(f"   ✅ Создано вопросов: {len(created_questions)}")
    print()
    print("   Теперь в меню будут отображаться данные!")
    print()
    return True


if __name__ == '__main__':
    seed_data()