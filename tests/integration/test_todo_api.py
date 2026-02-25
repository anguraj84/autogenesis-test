```python
import pytest
import httpx
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_post_todo_returns_201(test_workspace, test_user):
    # Arrange
    todo_data = {
        "title": "Test Todo",
        "description": "This is a test todo item."
    }
    headers = {
        "Authorization": f"Bearer {test_user['token']}"
    }
    async with AsyncClient(app=test_workspace['app'], base_url="http://test") as client:
        # Act
        response = await client.post("/api/v1/todos", json=todo_data, headers=headers)

    # Assert
    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["title"] == todo_data["title"]

@pytest.mark.asyncio
async def test_post_todo_unauthorized(test_workspace):
    # Arrange
    todo_data = {
        "title": "Test Todo",
        "description": "This is a test todo item."
    }
    async with AsyncClient(app=test_workspace['app'], base_url="http://test") as client:
        # Act
        response = await client.post("/api/v1/todos", json=todo_data)

    # Assert
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

@pytest.mark.asyncio
async def test_post_todo_validation_error(test_workspace, test_user):
    # Arrange
    todo_data = {
        "title": "",  # Invalid title
        "description": "This is a test todo item."
    }
    headers = {
        "Authorization": f"Bearer {test_user['token']}"
    }
    async with AsyncClient(app=test_workspace['app'], base_url="http://test") as client:
        # Act
        response = await client.post("/api/v1/todos", json=todo_data, headers=headers)

    # Assert
    assert response.status_code == 422
    assert "detail" in response.json()
    assert response.json()["detail"][0]["msg"] == "field required"
```