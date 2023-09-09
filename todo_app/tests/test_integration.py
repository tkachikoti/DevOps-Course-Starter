import requests

from todo_app.tests.utils import stub


def test_index_get_route(monkeypatch, client):
    monkeypatch.setattr(requests, 'get', stub)
    response = client.get('/')
    assert response.status_code == 200
    assert 'Item Name - Test One' in response.data.decode()


def test_add_todo_item_get_route(client):
    response = client.get('/add-todo-item')
    assert response.status_code == 200
    assert 'ADD TODO ITEM' in response.data.decode()
