"""
Flask сервер для системы Tech Support
API для управления вопросами, консультантами и ответами
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from database import Database
from models import TechSupportService
import json

app = Flask(__name__)
CORS(app)  # Разрешаем кросс-доменные запросы

# Инициализация БД и сервиса
db = Database()
service = TechSupportService(db)
service.load_data()


@app.route('/api/health', methods=['GET'])
def health_check():
    """Проверка работоспособности сервера"""
    return jsonify({'status': 'ok', 'message': 'Tech Support API is running'})


# ===== API для консультантов =====

@app.route('/api/consultants', methods=['GET'])
def get_consultants():
    """Получение списка всех консультантов"""
    consultants = service.get_consultants()
    return jsonify([c.to_dict() for c in consultants])


@app.route('/api/consultants', methods=['POST'])
def create_consultant():
    """Создание нового консультанта"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required = ['name', 'specialization', 'email']
    for field in required:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    
    consultant = service.add_consultant(
        name=data['name'],
        specialization=data['specialization'],
        email=data['email']
    )
    return jsonify(consultant.to_dict()), 201


# ===== API для вопросов =====

@app.route('/api/questions', methods=['GET'])
def get_questions():
    """Получение списка вопросов (с фильтрацией по статусу)"""
    status = request.args.get('status')
    questions = service.get_questions(status)
    return jsonify([q.to_dict() for q in questions])


@app.route('/api/questions/<int:question_id>', methods=['GET'])
def get_question(question_id):
    """Получение вопроса по ID"""
    question = service.get_question(question_id)
    if not question:
        return jsonify({'error': 'Question not found'}), 404
    return jsonify(question.to_dict())


@app.route('/api/questions', methods=['POST'])
def create_question():
    """Создание нового вопроса"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required = ['title', 'description', 'client_name']
    for field in required:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    
    priority = data.get('priority', 1)
    if not 1 <= priority <= 3:
        return jsonify({'error': 'Priority must be between 1 and 3'}), 400
    
    question = service.create_question(
        title=data['title'],
        description=data['description'],
        client_name=data['client_name'],
        priority=priority
    )
    return jsonify(question.to_dict()), 201


@app.route('/api/questions/<int:question_id>/assign', methods=['PUT'])
def assign_consultant(question_id):
    """Назначение консультанта на вопрос"""
    data = request.get_json()
    if not data or 'consultant_id' not in data:
        return jsonify({'error': 'consultant_id required'}), 400
    
    success = service.assign_consultant_to_question(
        question_id=question_id,
        consultant_id=data['consultant_id']
    )
    if not success:
        return jsonify({'error': 'Failed to assign consultant'}), 400
    
    question = service.get_question(question_id)
    return jsonify(question.to_dict())


@app.route('/api/questions/<int:question_id>/resolve', methods=['PUT'])
def resolve_question(question_id):
    """Отметить вопрос как решенный"""
    success = service.resolve_question(question_id)
    if not success:
        return jsonify({'error': 'Question not found'}), 404
    
    question = service.get_question(question_id)
    return jsonify(question.to_dict())


# ===== API для ответов =====

@app.route('/api/answers', methods=['POST'])
def create_answer():
    """Добавление ответа на вопрос"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required = ['question_id', 'consultant_id', 'content']
    for field in required:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    
    answer = service.add_answer(
        question_id=data['question_id'],
        consultant_id=data['consultant_id'],
        content=data['content']
    )
    if not answer:
        return jsonify({'error': 'Invalid question or consultant'}), 400
    
    return jsonify(answer.to_dict()), 201


# ===== API для статистики =====

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Получение статистики работы системы"""
    stats = service.get_statistics()
    return jsonify(stats)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)