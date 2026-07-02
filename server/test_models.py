"""
Модульные тесты для моделей данных
"Система технической поддержки"
"""

import unittest
import tempfile
import os
import warnings
import sqlite3
from models import Consultant, Question, Answer, TechSupportService
from database import Database

# Отключаем предупреждения ResourceWarning
warnings.filterwarnings("ignore", category=ResourceWarning)


class TestConsultant(unittest.TestCase):
    """Тесты для модели Consultant"""
    
    def setUp(self):
        self.consultant = Consultant(1, "Иван Петров", "Программное обеспечение", "ivan@tech.com")
    
    def test_initialization(self):
        self.assertEqual(self.consultant.id, 1)
        self.assertEqual(self.consultant.name, "Иван Петров")
        self.assertEqual(self.consultant.specialization, "Программное обеспечение")
        self.assertEqual(self.consultant.email, "ivan@tech.com")
        self.assertEqual(self.consultant.questions_handled, 0)
    
    def test_increment_handled(self):
        self.consultant.increment_handled()
        self.assertEqual(self.consultant.questions_handled, 1)
        self.consultant.increment_handled()
        self.consultant.increment_handled()
        self.assertEqual(self.consultant.questions_handled, 3)
    
    def test_to_dict(self):
        data = self.consultant.to_dict()
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['name'], "Иван Петров")
        self.assertEqual(data['specialization'], "Программное обеспечение")
        self.assertEqual(data['email'], "ivan@tech.com")
        self.assertEqual(data['questions_handled'], 0)
    
    def test_from_dict(self):
        data = {
            'id': 2,
            'name': 'Мария Сидорова',
            'specialization': 'Сетевое оборудование',
            'email': 'maria@tech.com',
            'questions_handled': 5
        }
        consultant = Consultant.from_dict(data)
        self.assertEqual(consultant.id, 2)
        self.assertEqual(consultant.name, "Мария Сидорова")
        self.assertEqual(consultant.questions_handled, 5)


class TestQuestion(unittest.TestCase):
    """Тесты для модели Question"""
    
    def setUp(self):
        self.question = Question(1, "Проблема с доступом", "Не могу войти в систему", "Клиент А", 3)
    
    def test_initialization(self):
        self.assertEqual(self.question.id, 1)
        self.assertEqual(self.question.title, "Проблема с доступом")
        self.assertEqual(self.question.status, Question.STATUS_NEW)
        self.assertEqual(self.question.priority, 3)
        self.assertIsNotNone(self.question.created_at)
        self.assertIsNone(self.question.consultant_id)
        self.assertEqual(len(self.question.answers), 0)
    
    def test_assign_consultant(self):
        self.question.assign_consultant(5)
        self.assertEqual(self.question.consultant_id, 5)
        self.assertEqual(self.question.status, Question.STATUS_IN_PROGRESS)
    
    def test_add_answer(self):
        answer = Answer(1, 1, 5, "Проверьте пароль")
        self.question.add_answer(answer)
        self.assertEqual(len(self.question.answers), 1)
        self.assertEqual(self.question.answers[0].content, "Проверьте пароль")
        self.assertEqual(self.question.status, Question.STATUS_IN_PROGRESS)
    
    def test_resolve(self):
        self.question.assign_consultant(5)
        self.question.resolve()
        self.assertEqual(self.question.status, Question.STATUS_RESOLVED)
    
    def test_close(self):
        self.question.close()
        self.assertEqual(self.question.status, Question.STATUS_CLOSED)
    
    def test_is_resolved(self):
        self.assertFalse(self.question.is_resolved)
        self.question.resolve()
        self.assertTrue(self.question.is_resolved)
        self.question.close()
        self.assertTrue(self.question.is_resolved)


class TestTechSupportService(unittest.TestCase):
    """Тесты для TechSupportService"""
    
    def setUp(self):
        """Подготовка к тестированию"""
        # Создаем временную БД
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.test_db_path = self.temp_db.name
        
        # Инициализируем БД и сервис
        self.db = Database(self.test_db_path)
        self.service = TechSupportService(self.db)
        self.service.load_data()
        
        print(f"\n[SETUP] Тестовая БД: {self.test_db_path}")
    
    def tearDown(self):
        """Очистка после тестирования"""
        # Закрываем соединение с БД
        try:
            if hasattr(self.db, 'conn'):
                self.db.conn.close()
        except:
            pass
        
        # Удаляем файл БД
        try:
            if os.path.exists(self.test_db_path):
                os.unlink(self.test_db_path)
                print(f"[TEARDOWN] Удалена БД: {self.test_db_path}")
        except Exception as e:
            print(f"[TEARDOWN] Ошибка удаления БД: {e}")
            # Пробуем удалить позже
            import time
            time.sleep(0.1)
            try:
                if os.path.exists(self.test_db_path):
                    os.unlink(self.test_db_path)
                    print(f"[TEARDOWN] Удалена БД (повторно): {self.test_db_path}")
            except:
                pass
    
    def test_add_consultant(self):
        """Тест добавления консультанта"""
        print("[TEST] test_add_consultant: Добавление консультанта...")
        
        consultant = self.service.add_consultant("Тест", "Тестирование", "test@test.com")
        self.assertEqual(consultant.name, "Тест")
        self.assertEqual(consultant.specialization, "Тестирование")
        self.assertEqual(consultant.id, 1)
        
        consultants = self.service.get_consultants()
        self.assertEqual(len(consultants), 1)
        
        print("[TEST] ✅ test_add_consultant пройден")
    
    def test_create_question(self):
        """Тест создания вопроса"""
        print("[TEST] test_create_question: Создание вопроса...")
        
        question = self.service.create_question(
            "Тестовый вопрос", 
            "Описание тестового вопроса", 
            "Тестовый клиент",
            2
        )
        self.assertEqual(question.title, "Тестовый вопрос")
        self.assertEqual(question.client_name, "Тестовый клиент")
        self.assertEqual(question.priority, 2)
        self.assertEqual(question.id, 1)
        
        questions = self.service.get_questions()
        self.assertEqual(len(questions), 1)
        
        print("[TEST] ✅ test_create_question пройден")
    
    def test_assign_consultant_to_question(self):
        """Тест назначения консультанта на вопрос"""
        print("[TEST] test_assign_consultant_to_question: Назначение консультанта...")
        
        # Создаем консультанта и вопрос
        consultant = self.service.add_consultant("Тест", "Тестирование", "test@test.com")
        question = self.service.create_question("Тест", "Описание", "Клиент")
        
        # Назначаем
        result = self.service.assign_consultant_to_question(question.id, consultant.id)
        self.assertTrue(result)
        
        # Проверяем
        updated_q = self.service.get_question(question.id)
        self.assertEqual(updated_q.consultant_id, consultant.id)
        self.assertEqual(updated_q.status, Question.STATUS_IN_PROGRESS)
        
        updated_c = self.service.get_consultant(consultant.id)
        self.assertEqual(updated_c.questions_handled, 1)
        
        print("[TEST] ✅ test_assign_consultant_to_question пройден")
    
    def test_add_answer(self):
        """Тест добавления ответа"""
        print("[TEST] test_add_answer: Добавление ответа...")
        
        consultant = self.service.add_consultant("Тест", "Тестирование", "test@test.com")
        question = self.service.create_question("Тест", "Описание", "Клиент")
        self.service.assign_consultant_to_question(question.id, consultant.id)
        
        answer = self.service.add_answer(question.id, consultant.id, "Тестовый ответ")
        self.assertIsNotNone(answer)
        self.assertEqual(answer.content, "Тестовый ответ")
        
        updated_q = self.service.get_question(question.id)
        self.assertEqual(len(updated_q.answers), 1)
        self.assertEqual(updated_q.answers[0].content, "Тестовый ответ")
        
        print("[TEST] ✅ test_add_answer пройден")
    
    def test_resolve_question(self):
        """Тест отметки вопроса как решенного"""
        print("[TEST] test_resolve_question: Отметка как решенного...")
        
        consultant = self.service.add_consultant("Тест", "Тестирование", "test@test.com")
        question = self.service.create_question("Тест", "Описание", "Клиент")
        self.service.assign_consultant_to_question(question.id, consultant.id)
        
        result = self.service.resolve_question(question.id)
        self.assertTrue(result)
        
        updated_q = self.service.get_question(question.id)
        self.assertEqual(updated_q.status, Question.STATUS_RESOLVED)
        
        print("[TEST] ✅ test_resolve_question пройден")
    
    def test_get_statistics(self):
        """Тест получения статистики"""
        print("[TEST] test_get_statistics: Получение статистики...")
        
        # Создаем данные
        c1 = self.service.add_consultant("C1", "S1", "c1@test.com")
        c2 = self.service.add_consultant("C2", "S2", "c2@test.com")
        
        q1 = self.service.create_question("Q1", "Desc1", "Client1")
        q2 = self.service.create_question("Q2", "Desc2", "Client2")
        
        self.service.assign_consultant_to_question(q1.id, c1.id)
        self.service.assign_consultant_to_question(q2.id, c2.id)
        self.service.add_answer(q1.id, c1.id, "Answer1")
        self.service.resolve_question(q1.id)
        
        stats = self.service.get_statistics()
        self.assertEqual(stats['total_questions'], 2)
        self.assertEqual(stats['consultants_count'], 2)
        self.assertEqual(stats['answers_count'], 1)
        self.assertEqual(stats['resolved_count'], 1)
        self.assertEqual(stats['by_status'][Question.STATUS_RESOLVED], 1)
        self.assertEqual(stats['by_status'][Question.STATUS_IN_PROGRESS], 1)
        
        print("[TEST] ✅ test_get_statistics пройден")


if __name__ == '__main__':
    # Запускаем все тесты с подробным выводом
    unittest.main(verbosity=2)