import requests

from todo_app.tests.test_utils import stub


def test_index_get_route(monkeypatch, client):
    monkeypatch.setattr(requests, 'get', stub)
    response = client.get('/')
    assert response.status_code == 200
    assert 'Item Name - Test One' in response.data.decode()


def test_add_todo_item_get_route(client):
    response = client.get('/add-todo-item')
    assert response.status_code == 200
    assert 'ADD TODO ITEM' in response.data.decode()


def test_view_model_todo_items(example_view_model_items):
    assert len(example_view_model_items.todo_items) > 0
    assert all(
        item.status == "To Do" for item in example_view_model_items.todo_items
    )


def test_view_model_doing_items(example_view_model_items):
    assert len(example_view_model_items.doing_items) > 0
    assert all(
        item.status == "Doing" for item in example_view_model_items.doing_items
    )


def test_view_model_done_items(example_view_model_items):
    assert len(example_view_model_items.done_items) > 0
    assert all(
        item.status == "Done" for item in example_view_model_items.done_items
    )
