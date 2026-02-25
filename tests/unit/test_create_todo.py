```python
import pytest
from httpx import AsyncClient
from pytest_mock import MockerFixture
from sqlalchemy.ext.asyncio import AsyncSession
from src.todo.routes.create_todo import create_todo

@pytest.mark.asyncio
async def test_create_todo_success(test_client: AsyncClient, mocker: MockerFixture):
    # Arrange
    mock_session = mocker.patch('src.todo.routes.create_todo.AsyncSession', autospec=True)
    mock_session.return_value.__aenter__.return_value = mocker.Mock(spec=AsyncSession)
    todo_data = {"title": "Test Todo", "description": "Test Description"}

    # Act
    response = await test_client.post("/todos", json=todo_data)

    # Assert
    assert response.status_code == 201
    assert response.json() == {"id": 1, "title": "Test Todo", "description": "Test Description"}

@pytest.mark.asyncio
async def test_create_todo_validation_error(test_client: AsyncClient, mocker: MockerFixture):
    # Arrange
    mock_session = mocker.patch('src.todo.routes.create_todo.AsyncSession', autospec=True)
    mock_session.return_value.__aenter__.return_value = mocker.Mock(spec=AsyncSession)
    invalid_todo_data = {"title": ""}  # Missing required fields

    # Act
    response = await test_client.post("/todos", json=invalid_todo_data)

    # Assert
    assert response.status_code == 422
    assert "detail" in response.json()

@pytest.mark.asyncio
async def test_create_todo_server_error(test_client: AsyncClient, mocker: MockerFixture):
    # Arrange
    mock_session = mocker.patch('src.todo.routes.create_todo.AsyncSession', autospec=True)
    mock_session.return_value.__aenter__.side_effect = Exception("Database error")
    todo_data = {"title": "Test Todo", "description": "Test Description"}

    # Act
    response = await test_client.post("/todos", json=todo_data)

    # Assert
    assert response.status_code == 500
    assert response.json() == {"detail": "Internal Server Error"}
```