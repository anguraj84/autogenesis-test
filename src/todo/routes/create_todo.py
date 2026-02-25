from flask import Blueprint, request, jsonify
from src.todo.models.todo_item import TodoItem, TodoItemRepository
from datetime import datetime
from werkzeug.exceptions import BadRequest

create_todo_bp = Blueprint('create_todo', __name__)

@create_todo_bp.route('/todo', methods=['POST'])
def create_todo():
    try:
        data = request.get_json()
        if not data:
            raise BadRequest("Invalid JSON data")

        title = data.get('title')
        description = data.get('description')
        due_date_str = data.get('due_date')
        status = data.get('status', 'pending')

        if not title:
            raise BadRequest("Title is required")

        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            except ValueError:
                raise BadRequest("Invalid date format, should be YYYY-MM-DD")
        else:
            due_date = None

        todo_item = TodoItem(title=title, description=description, due_date=due_date, status=status)
        TodoItemRepository.save(todo_item)

        return jsonify({"message": "Todo item created successfully", "todo": todo_item.to_dict()}), 201

    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred"}), 500