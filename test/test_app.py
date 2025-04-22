import json
import pytest
from app import app

# Включаем тестовый режим
app.testing = True

def test_api_posts():
    with app.test_client() as client:
        response = client.get('/api/posts')
        assert response.status_code == 200

        data = response.get_json()
        assert type(data) == list
        assert len(data) > 0

        post = data[0]
        assert "poster_name" in post
        assert "content" in post
        assert "pk" in post

def test_api_post_by_id():
    with app.test_client() as client:
        response = client.get('/api/posts/1')
        assert response.status_code == 200

        data = response.get_json()
        assert type(data) == dict

        assert "poster_name" in data
        assert "content" in data
        assert "pk" in data