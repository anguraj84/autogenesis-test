```python
import pytest
from unittest.mock import AsyncMock
from src.todo.models.todo_item import TodoItem

@pytest.mark.asyncio
async def test_todo_item_creation_happy_path(mocker, db_session):
    # Arrange
    mocker.patch('src.todo.models.todo_item.TodoItem.save', new_callable=AsyncMock)
    todo_data = {
        "title": "Test Todo",
        "description": "This is a test todo item",
        "completed": False
    }
    todo_item = TodoItem(**todo_data)

    # Act
    await todo_item.save(db_session)

    # Assert
    todo_item.save.assert_awaited_once_with(db_session)
    assert todo_item.title == "Test Todo"
    assert todo_item.description == "This is a test todo item"
    assert not todo_item.completed

@pytest.mark.asyncio
async def test_todo_item_invalid_data(mocker, db_session):
    # Arrange
    mocker.patch('src.todo.models.todo_item.TodoItem.save', new_callable=AsyncMock)
    invalid_todo_data = {
        "title": "",  # Invalid title
        "description": "This is a test todo item",
        "completed": False
    }
    todo_item = TodoItem(**invalid_todo_data)

    # Act
    with pytest.raises(ValueError) as excinfo:
        await todo_item.save(db_session)

    # Assert
    assert "Invalid title" in str(excinfo.value)
    todo_item.save.assert_not_awaited()

@pytest.mark.asyncio
async def test_todo_item_edge_case(mocker, db_session):
    # Arrange
    mocker.patch('src.todo.models.todo_item.TodoItem.save', new_callable=AsyncMock)
    edge_case_data = {
        "title": "x" * 256,  # Edge case: title length
        "description": "Edge case description",
        "completed": False
    }
    todo_item = TodoItem(**edge_case_data)

    # Act
    await todo_item.save(db_session)

    # Assert
    todo_item.save.assert_awaited_once_with(db_session)
    assert todo_item.title == "x" * 256
    assert todo_item.description == "Edge case description"
    assert not todo_item.completed
```