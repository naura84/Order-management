import sys
from pathlib import Path
import os

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

os.environ["API_KEY"] = "test-api-key"

from main import app


client = TestClient(app)


@pytest.fixture
def api_client():
    return client


@pytest.fixture
def headers():
    return {
        "X-API-Key": "test-api-key"
    }