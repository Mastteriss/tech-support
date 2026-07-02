"""
Модуль для работы с базой данных SQLite
"""

import sqlite3
from typing import List, Optional
from models import Consultant, Question, Answer


class Database:
    """Класс для управления подключением и операциями с БД"""
    
    def __init__(self, db_path: str = 'tech_support.db'):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Инициализация базы данных и создание таблиц"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Таблица консультантов
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS consultants (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    specialization TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    questions_handled INTEGER DEFAULT 0
                )
            ''')
            
            # Таблица вопросов
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS questions (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    client_name TEXT NOT NULL,
                    priority INTEGER DEFAULT 1,
                    status TEXT DEFAULT 'new',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    consultant_id INTEGER,
                    FOREIGN KEY (consultant_id) REFERENCES consultants(id)
                )
            ''')
            
            # Таблица ответов
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS answers (
                    id INTEGER PRIMARY KEY,
                    question_id INTEGER NOT NULL,
                    consultant_id INTEGER NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (question_id) REFERENCES questions(id),
                    FOREIGN KEY (consultant_id) REFERENCES consultants(id)
                )
            ''')
            
            conn.commit()
    
    # Методы для Consultants
    def get_consultants(self) -> List[Consultant]:
        """Получает всех консультантов"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM consultants')
            rows = cursor.fetchall()
            
            consultants = []
            for row in rows:
                consultant = Consultant(
                    id=row['id'],
                    name=row['name'],
                    specialization=row['specialization'],
                    email=row['email']
                )
                consultant._questions_handled = row['questions_handled']
                consultants.append(consultant)
            return consultants
    
    def save_consultant(self, consultant: Consultant):
        """Сохраняет консультанта в БД"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO consultants 
                (id, name, specialization, email, questions_handled)
                VALUES (?, ?, ?, ?, ?)
            ''', (consultant.id, consultant.name, consultant.specialization,
                  consultant.email, consultant.questions_handled))
            conn.commit()
    
    def update_consultant(self, consultant: Consultant):
        """Обновляет данные консультанта"""
        self.save_consultant(consultant)
    
    # Методы для Questions
    def get_questions(self) -> List[Question]:
        """Получает все вопросы"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM questions')
            rows = cursor.fetchall()
            
            questions = []
            for row in rows:
                question = Question(
                    id=row['id'],
                    title=row['title'],
                    description=row['description'],
                    client_name=row['client_name'],
                    priority=row['priority']
                )
                question.status = row['status']
                question.created_at = row['created_at']
                question.updated_at = row['updated_at']
                question.consultant_id = row['consultant_id']
                questions.append(question)
            return questions
    
    def save_question(self, question: Question):
        """Сохраняет вопрос в БД"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO questions
                (id, title, description, client_name, priority, 
                 status, created_at, updated_at, consultant_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (question.id, question.title, question.description,
                  question.client_name, question.priority, question.status,
                  question.created_at.isoformat(), question.updated_at.isoformat(),
                  question.consultant_id))
            conn.commit()
    
    def update_question(self, question: Question):
        """Обновляет данные вопроса"""
        self.save_question(question)
    
    # Методы для Answers
    def get_answers(self) -> List[Answer]:
        """Получает все ответы"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM answers')
            rows = cursor.fetchall()
            
            answers = []
            for row in rows:
                answer = Answer(
                    id=row['id'],
                    question_id=row['question_id'],
                    consultant_id=row['consultant_id'],
                    content=row['content']
                )
                answer.created_at = row['created_at']
                answers.append(answer)
            return answers
    
    def save_answer(self, answer: Answer):
        """Сохраняет ответ в БД"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO answers
                (id, question_id, consultant_id, content, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (answer.id, answer.question_id, answer.consultant_id,
                  answer.content, answer.created_at.isoformat()))
            conn.commit()
    
    def clear_all(self):
        """Очищает все таблицы (для тестов)"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM answers')
            cursor.execute('DELETE FROM questions')
            cursor.execute('DELETE FROM consultants')
            conn.commit()