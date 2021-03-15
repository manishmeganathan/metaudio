import pytest
from audioserver import app as flask_app


@pytest.fixture
def app():
    """doc"""
    yield flask_app


@pytest.fixture
def client(app):
    """doc"""
    return app.test_client()
