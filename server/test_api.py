"""
Тесты API сервера
"Система технической поддержки"

Содержит тесты для проверки всех REST API эндпоинтов.
"""

import unittest
import json
import tempfile
import os
import sqlite3
from app import app, service, db


class TestAPI(unittest.TestCase):
    """Тесты API эндпоинтов"""
    
    def setUp(self):
        """Подготовка к тестированию - создание тестовой БД"""
        # Создаем тестовый клиент Flask
        self.app = app.test_client()
        
        # Создаем временный файл для базы данных
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        
        # Сохраняем путь к тестовой БД
        self.test_db_path = self.temp_db.name
        
        # Настраиваем приложение на использование тестовой БД
        db.db_path = self.test_db_path
        
        # Инициализируем базу данных
        db._init_db()
        
        # Загружаем данные в сервис
        service.db = db
        service.load_data()
        
        print(f"\n[SETUP] Создана тестовая БД: {self.test_db_path}")
    
    def tearDown(self):
        """Очистка после тестирования - закрытие БД и удаление файла"""
        # Закрываем все соединения с БД
        try:
            # Закрываем соединение в db, если оно открыто
            if hasattr(db, 'conn'):
                db.conn.close()
        except:
            pass
        
        # Удаляем файл БД
        try:
            if os.path.exists(self.test_db_path):
                os.unlink(self.test_db_path)
                print(f"[TEARDOWN] Удалена тестовая БД: {self.test_db_path}")
        except Exception as e:
            print(f"[TEARDOWN] Ошибка удаления БД: {e}")
            # Если не удалось удалить, попробуем позже
            import time
            time.sleep(0.1)
            try:
                os.unlink(self.test_db_path)
                print(f"[TEARDOWN] Удалена тестовая БД (повторно): {self.test_db_path}")
            except:
                pass
    
    def test_health_check(self):
        """Тест проверки работоспособности сервера"""
        print("\n[TEST] test_health_check: Проверка работоспособности...")
        
        response = self.app.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['message'], 'Tech Support API is running')
        
        print("[TEST] ✅ test_health_check пройден")
    
    def test_create_and_get_consultant(self):
        """Тест создания и получения консультанта"""
        print("\n[TEST] test_create_and_get_consultant: Тест консультанта...")
        
        # Создание
        response = self.app.post('/api/consultants', 
                                json={'name': 'Тест', 'specialization': 'Тестирование', 
                                      'email': 'test@test.com'})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        consultant_id = data['id']
        print(f"[TEST] ✅ Создан консультант ID: {consultant_id}")
        
        # Получение списка
        response = self.app.get('/api/consultants')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'Тест')
        
        print("[TEST] ✅ test_create_and_get_consultant пройден")
    
    def test_create_question(self):
        """Тест создания вопроса"""
        print("\n[TEST] test_create_question: Тест создания вопроса...")
        
        response = self.app.post('/api/questions', 
                                json={'title': 'Тестовый вопрос', 
                                     'description': 'Описание',
                                     'client_name': 'Клиент',
                                     'priority': 2})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Тестовый вопрос')
        self.assertEqual(data['status'], 'new')
        
        print(f"[TEST] ✅ Создан вопрос ID: {data['id']}")
        print("[TEST] ✅ test_create_question пройден")
    
    def test_get_questions_filter(self):
        """Тест фильтрации вопросов по статусу"""
        print("\n[TEST] test_get_questions_filter: Тест фильтрации...")
        
        # Создаем консультанта
        self.app.post('/api/consultants', 
                     json={'name': 'Тест', 'specialization': 'Тестирование', 
                           'email': 'test@test.com'})
        
        # Создаем вопросы
        r1 = self.app.post('/api/questions', 
                          json={'title': 'Q1', 'description': 'D1', 
                                'client_name': 'C1', 'priority': 1})
        q1 = json.loads(r1.data)
        print(f"[TEST] ✅ Создан вопрос Q1 ID: {q1['id']}")
        
        r2 = self.app.post('/api/questions', 
                          json={'title': 'Q2', 'description': 'D2', 
                                'client_name': 'C2', 'priority': 2})
        q2 = json.loads(r2.data)
        print(f"[TEST] ✅ Создан вопрос Q2 ID: {q2['id']}")
        
        # Отмечаем q1 как решенный
        self.app.put(f'/api/questions/{q1["id"]}/resolve')
        print(f"[TEST] ✅ Вопрос Q1 отмечен как решенный")
        
        # Проверяем фильтр по статусу
        response = self.app.get('/api/questions?status=resolved')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['id'], q1['id'])
        
        print("[TEST] ✅ test_get_questions_filter пройден")
    
    def test_assign_consultant_flow(self):
        """Тест назначения консультанта на вопрос"""
        print("\n[TEST] test_assign_consultant_flow: Тест назначения...")
        
        # Создаем консультанта
        r1 = self.app.post('/api/consultants', 
                          json={'name': 'Тест', 'specialization': 'Тестирование', 
                                'email': 'test@test.com'})
        consultant = json.loads(r1.data)
        print(f"[TEST] ✅ Создан консультант ID: {consultant['id']}")
        
        # Создаем вопрос
        r2 = self.app.post('/api/questions', 
                          json={'title': 'Тест', 'description': 'Описание', 
                                'client_name': 'Клиент', 'priority': 1})
        question = json.loads(r2.data)
        print(f"[TEST] ✅ Создан вопрос ID: {question['id']}")
        
        # Назначаем консультанта
        response = self.app.put(f'/api/questions/{question["id"]}/assign',
                               json={'consultant_id': consultant['id']})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['consultant_id'], consultant['id'])
        self.assertEqual(data['status'], 'in_progress')
        
        print("[TEST] ✅ test_assign_consultant_flow пройден")
    
    def test_add_answer(self):
        """Тест добавления ответа на вопрос"""
        print("\n[TEST] test_add_answer: Тест добавления ответа...")
        
        # Создаем консультанта
        r1 = self.app.post('/api/consultants', 
                          json={'name': 'Тест', 'specialization': 'Тестирование', 
                                'email': 'test@test.com'})
        consultant = json.loads(r1.data)
        print(f"[TEST] ✅ Создан консультант ID: {consultant['id']}")
        
        # Создаем вопрос
        r2 = self.app.post('/api/questions', 
                          json={'title': 'Тест', 'description': 'Описание', 
                                'client_name': 'Клиент', 'priority': 1})
        question = json.loads(r2.data)
        print(f"[TEST] ✅ Создан вопрос ID: {question['id']}")
        
        # Назначаем консультанта
        self.app.put(f'/api/questions/{question["id"]}/assign',
                    json={'consultant_id': consultant['id']})
        print(f"[TEST] ✅ Назначен консультант на вопрос")
        
        # Добавляем ответ
        answer_content = 'Тестовый ответ на вопрос'
        response = self.app.post('/api/answers',
                                json={'question_id': question['id'],
                                     'consultant_id': consultant['id'],
                                     'content': answer_content})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['content'], answer_content)
        print(f"[TEST] ✅ Добавлен ответ ID: {data['id']}")
        
        # Проверяем, что ответ сохранился
        response = self.app.get(f'/api/questions/{question["id"]}')
        data = json.loads(response.data)
        self.assertEqual(len(data['answers']), 1)
        self.assertEqual(data['answers'][0]['content'], answer_content)
        
        print("[TEST] ✅ test_add_answer пройден")
    
    def test_resolve_question(self):
        """Тест отметки вопроса как решенного"""
        print("\n[TEST] test_resolve_question: Тест отметки как решенного...")
        
        # Создаем вопрос
        r = self.app.post('/api/questions', 
                         json={'title': 'Тест', 'description': 'Описание', 
                               'client_name': 'Клиент', 'priority': 1})
        question = json.loads(r.data)
        print(f"[TEST] ✅ Создан вопрос ID: {question['id']}")
        
        # Решаем
        response = self.app.put(f'/api/questions/{question["id"]}/resolve')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'resolved')
        
        print("[TEST] ✅ test_resolve_question пройден")
    
    def test_statistics(self):
        """Тест получения статистики"""
        print("\n[TEST] test_statistics: Тест статистики...")
        
        # Создаем консультантов
        r1 = self.app.post('/api/consultants', 
                          json={'name': 'C1', 'specialization': 'S1', 
                                'email': 'c1@test.com'})
        c1 = json.loads(r1.data)
        print(f"[TEST] ✅ Создан консультант C1 ID: {c1['id']}")
        
        r2 = self.app.post('/api/consultants', 
                          json={'name': 'C2', 'specialization': 'S2', 
                                'email': 'c2@test.com'})
        c2 = json.loads(r2.data)
        print(f"[TEST] ✅ Создан консультант C2 ID: {c2['id']}")
        
        # Создаем вопросы
        r3 = self.app.post('/api/questions', 
                          json={'title': 'Q1', 'description': 'D1', 
                                'client_name': 'Client1', 'priority': 1})
        q1 = json.loads(r3.data)
        print(f"[TEST] ✅ Создан вопрос Q1 ID: {q1['id']}")
        
        r4 = self.app.post('/api/questions', 
                          json={'title': 'Q2', 'description': 'D2', 
                                'client_name': 'Client2', 'priority': 2})
        q2 = json.loads(r4.data)
        print(f"[TEST] ✅ Создан вопрос Q2 ID: {q2['id']}")
        
        # Назначаем и решаем
        self.app.put(f'/api/questions/{q1["id"]}/assign', 
                    json={'consultant_id': c1['id']})
        self.app.put(f'/api/questions/{q1["id"]}/resolve')
        print(f"[TEST] ✅ Вопрос Q1 решен")
        
        self.app.put(f'/api/questions/{q2["id"]}/assign', 
                    json={'consultant_id': c2['id']})
        print(f"[TEST] ✅ Вопрос Q2 в работе")
        
        # Получаем статистику
        response = self.app.get('/api/statistics')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertEqual(data['total_questions'], 2)
        self.assertEqual(data['consultants_count'], 2)
        self.assertEqual(data['resolved_count'], 1)
        
        print(f"[TEST] ✅ Статистика: Всего вопросов={data['total_questions']}, "
              f"Консультантов={data['consultants_count']}, "
              f"Решено={data['resolved_count']}")
        print("[TEST] ✅ test_statistics пройден")


if __name__ == '__main__':
    # Запускаем все тесты с подробным выводом
    unittest.main(verbosity=2)