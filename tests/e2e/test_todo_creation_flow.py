```python
import pytest
import httpx
from pytest_mock import MockerFixture

@pytest.mark.asyncio
async def test_navigate_to_todo_creation_page(client: httpx.AsyncClient):
    # Arrange
    url = "/todo/create"

    # Act
    response = await client.get(url)

    # Assert
    assert response.status_code == 200
    assert "Create New To-Do" in response.text

@pytest.mark.asyncio
async def test_fill_in_todo_details(client: httpx.AsyncClient):
    # Arrange
    url = "/todo/create"
    todo_data = {
        "title": "Test To-Do",
        "description": "This is a test to-do item."
    }

    # Act
    response = await client.post(url, data=todo_data)

    # Assert
    assert response.status_code == 200
    assert "Test To-Do" in response.text
    assert "This is a test to-do item." in response.text

@pytest.mark.asyncio
async def test_submit_form_and_verify_creation(client: httpx.AsyncClient, mocker: MockerFixture):
    # Arrange
    url = "/todo/create"
    todo_data = {
        "title": "Test To-Do",
        "description": "This is a test to-do item."
    }
    mock_db = mocker.patch("app.database.get_db")
    mock_db.return_value.execute.return_value = 1  # Mock DB response for successful insert

    # Act
    response = await client.post(url, data=todo_data)

    # Assert
    assert response.status_code == 200
    assert "To-Do created successfully" in response.text
    mock_db.return_value.execute.assert_called_once()
```