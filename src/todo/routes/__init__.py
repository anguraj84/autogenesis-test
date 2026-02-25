from flask import Blueprint, request, jsonify
from src.todo.models.todo_item import TodoItem
from src.todo.routes.create_todo import create_todo_item

todo_bp = Blueprint('todo', __name__)

@todo_bp.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid input'}), 400

    title = data.get('title')
    description = data.get('description')
    due_date = data.get('due_date')
    status = data.get('status')

    if not title or not due_date or not status:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        todo_item = create_todo_item(title, description, due_date, status)
        return jsonify(todo_item.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred'}), 500