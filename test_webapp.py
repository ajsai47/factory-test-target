"""Tests for webapp module."""
from webapp import app


def test_hello_endpoint():
    """Test the /hello endpoint."""
    client = app.test_client()
    response = client.get('/hello')

    assert response.status_code == 200
    assert response.json == {"message": "hello from factory"}