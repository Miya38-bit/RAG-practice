import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi.testclient import TestClient
from main import app
from dependencies import get_openai_client, get_search_client

@pytest.fixture
def mock_openai_client():
    return AsyncMock()

@pytest.fixture
def mock_search_client():
    return MagicMock()

@pytest.fixture
def client(mock_openai_client, mock_search_client):
    # 依存関係をモックに置き換え
    app.dependency_overrides[get_openai_client] = lambda: mock_openai_client
    app.dependency_overrides[get_search_client] = lambda: mock_search_client
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


