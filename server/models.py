"""
Модели данных предметной области "Техподдержка"
"""

from datetime import datetime
from typing import List, Optional
import json


class Consultant:
    """Модель консультанта"""
    
    def __init__(self, id: int, name: str, specialization: str, email: str):
        self.id = id
        self.name = name
        self.specialization = specialization
        self.email = email
        self._questions_handled = 0
    
    @property
    def questions_handled(self) -> int:
        """Количество обработанных вопросов"""
        return self._questions_handled
    
    def increment_handled(self):
        """Увеличивает счетчик обработанных вопросов"""
        self._questions_handled += 1
    
    def to_dict(self) -> dict:
        """Преобразует объект в словарь для JSON"""
        return {
            'id': self.id,
            'name': self.name,
            'specialization': self.specialization,
            'email': self.email,
            'questions_handled': self.questions_handled
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Consultant':
        """Создает объект из словаря"""
        consultant = cls(
            id=data['id'],
            name=data['name'],
            specialization=data['specialization'],
            email=data['email']
        )
        consultant._questions_handled = data.get('questions_handled', 0)
        return consultant


class Question:
    """Модель вопроса"""
    
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_RESOLVED = 'resolved'
    STATUS_CLOSED = 'closed'
    
    STATUSES = [STATUS_NEW, STATUS_IN_PROGRESS, STATUS_RESOLVED, STATUS_CLOSED]
    
    def __init__(self, id: int, title: str, description: str, 
                 client_name: str, priority: int = 1):
        self.id = id
        self.title = title
        self.description = description
        self.client_name = client_name
        self.priority = priority  # 1 - низкий, 2 - средний, 3 - высокий
        self.status = self.STATUS_NEW
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.consultant_id: Optional[int] = None
        self._answers: List['Answer'] = []
    
    def assign_consultant(self, consultant_id: int):
        """Назначает консультанта на вопрос"""
        self.consultant_id = consultant_id
        if self.status == self.STATUS_NEW:
            self.status = self.STATUS_IN_PROGRESS
        self.updated_at = datetime.now()
    
    def add_answer(self, answer: 'Answer'):
        """Добавляет ответ к вопросу"""
        self._answers.append(answer)
        self.updated_at = datetime.now()
        if self.status != self.STATUS_RESOLVED:
            self.status = self.STATUS_IN_PROGRESS
    
    def resolve(self):
        """Отмечает вопрос как решенный"""
        self.status = self.STATUS_RESOLVED
        self.updated_at = datetime.now()
    
    def close(self):
        """Закрывает вопрос"""
        self.status = self.STATUS_CLOSED
        self.updated_at = datetime.now()
    
    @property
    def answers(self) -> List['Answer']:
        """Возвращает список ответов"""
        return self._answers.copy()
    
    @property
    def is_resolved(self) -> bool:
        """Проверяет, решен ли вопрос"""
        return self.status in [self.STATUS_RESOLVED, self.STATUS_CLOSED]
    
    def to_dict(self) -> dict:
        """Преобразует объект в словарь для JSON"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'client_name': self.client_name,
            'priority': self.priority,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'consultant_id': self.consultant_id,
            'answers': [a.to_dict() for a in self._answers]
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Question':
        """Создает объект из словаря"""
        question = cls(
            id=data['id'],
            title=data['title'],
            description=data['description'],
            client_name=data['client_name'],
            priority=data.get('priority', 1)
        )
        question.status = data.get('status', cls.STATUS_NEW)
        question.consultant_id = data.get('consultant_id')
        if 'created_at' in data:
            question.created_at = datetime.fromisoformat(data['created_at'])
        if 'updated_at' in data:
            question.updated_at = datetime.fromisoformat(data['updated_at'])
        # Восстанавливаем ответы
        if 'answers' in data:
            question._answers = [Answer.from_dict(a) for a in data['answers']]
        return question


class Answer:
    """Модель ответа на вопрос"""
    
    def __init__(self, id: int, question_id: int, consultant_id: int, 
                 content: str):
        self.id = id
        self.question_id = question_id
        self.consultant_id = consultant_id
        self.content = content
        self.created_at = datetime.now()
    
    def to_dict(self) -> dict:
        """Преобразует объект в словарь для JSON"""
        return {
            'id': self.id,
            'question_id': self.question_id,
            'consultant_id': self.consultant_id,
            'content': self.content,
            'created_at': self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Answer':
        """Создает объект из словаря"""
        answer = cls(
            id=data['id'],
            question_id=data['question_id'],
            consultant_id=data['consultant_id'],
            content=data['content']
        )
        if 'created_at' in data:
            answer.created_at = datetime.fromisoformat(data['created_at'])
        return answer


class TechSupportService:
    """Сервис для управления данными (бизнес-логика)"""
    
    def __init__(self, db):
        self.db = db
        self._consultants: List[Consultant] = []
        self._questions: List[Question] = []
        self._answers: List[Answer] = []
    
    def load_data(self):
        """Загружает данные из БД"""
        self._consultants = self.db.get_consultants()
        self._questions = self.db.get_questions()
        self._answers = self.db.get_answers()
        
        # Восстанавливаем связи
        for question in self._questions:
            question._answers = [a for a in self._answers 
                                if a.question_id == question.id]
    
    def get_consultants(self) -> List[Consultant]:
        """Возвращает список всех консультантов"""
        return self._consultants.copy()
    
    def get_consultant(self, consultant_id: int) -> Optional[Consultant]:
        """Возвращает консультанта по ID"""
        for c in self._consultants:
            if c.id == consultant_id:
                return c
        return None
    
    def add_consultant(self, name: str, specialization: str, email: str) -> Consultant:
        """Добавляет нового консультанта"""
        new_id = max([c.id for c in self._consultants] + [0]) + 1
        consultant = Consultant(new_id, name, specialization, email)
        self._consultants.append(consultant)
        self.db.save_consultant(consultant)
        return consultant
    
    def get_questions(self, status: str = None) -> List[Question]:
        """Возвращает вопросы с возможной фильтрацией по статусу"""
        if status:
            return [q for q in self._questions if q.status == status]
        return self._questions.copy()
    
    def get_question(self, question_id: int) -> Optional[Question]:
        """Возвращает вопрос по ID"""
        for q in self._questions:
            if q.id == question_id:
                return q
        return None
    
    def create_question(self, title: str, description: str, 
                        client_name: str, priority: int = 1) -> Question:
        """Создает новый вопрос"""
        new_id = max([q.id for q in self._questions] + [0]) + 1
        question = Question(new_id, title, description, client_name, priority)
        self._questions.append(question)
        self.db.save_question(question)
        return question
    
    def assign_consultant_to_question(self, question_id: int, consultant_id: int) -> bool:
        """Назначает консультанта на вопрос"""
        question = self.get_question(question_id)
        consultant = self.get_consultant(consultant_id)
        if not question or not consultant:
            return False
        question.assign_consultant(consultant_id)
        consultant.increment_handled()
        self.db.update_question(question)
        self.db.update_consultant(consultant)
        return True
    
    def add_answer(self, question_id: int, consultant_id: int, content: str) -> Optional[Answer]:
        """Добавляет ответ на вопрос"""
        question = self.get_question(question_id)
        consultant = self.get_consultant(consultant_id)
        if not question or not consultant:
            return None
        
        new_id = max([a.id for a in self._answers] + [0]) + 1
        answer = Answer(new_id, question_id, consultant_id, content)
        self._answers.append(answer)
        question.add_answer(answer)
        self.db.save_answer(answer)
        self.db.update_question(question)
        return answer
    
    def resolve_question(self, question_id: int) -> bool:
        """Отмечает вопрос как решенный"""
        question = self.get_question(question_id)
        if not question:
            return False
        question.resolve()
        self.db.update_question(question)
        return True
    
    def get_statistics(self) -> dict:
        """Возвращает статистику по работе"""
        total = len(self._questions)
        by_status = {status: 0 for status in Question.STATUSES}
        for q in self._questions:
            by_status[q.status] = by_status.get(q.status, 0) + 1
        
        return {
            'total_questions': total,
            'by_status': by_status,
            'consultants_count': len(self._consultants),
            'answers_count': len(self._answers),
            'resolved_count': len([q for q in self._questions if q.is_resolved])
        }