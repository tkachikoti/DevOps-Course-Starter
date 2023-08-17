import json
import os
import requests

import pytest
from dotenv import find_dotenv, load_dotenv

from todo_app.data.view_model import ViewModel
from todo_app.data.item import Item
from todo_app import app


@pytest.fixture
def load_environment_variables():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)


@pytest.fixture
def client(load_environment_variables):
    # Create the new app.
    test_app = app.create_app()
    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client


@pytest.fixture
def example_view_model_items():
    # Create mock items
    item1 = Item(title="Task 1", id_list=TRELLO_TODO_LIST_ID())
    item2 = Item(title="Task 2", id_list=TRELLO_DOING_LIST_ID())
    item3 = Item(title="Task 3", id_list=TRELLO_DONE_LIST_ID())
    item4 = Item(title="Task 4", id_list=TRELLO_TODO_LIST_ID())
    item5 = Item(title="Task 5", id_list=TRELLO_DOING_LIST_ID())
    item6 = Item(title="Task 6", id_list=TRELLO_DONE_LIST_ID())

    return ViewModel([item1, item2, item3, item4, item5, item6])


def TRELLO_TODO_LIST_ID():
    return os.getenv("TRELLO_TODO_LIST_ID")


def TRELLO_DOING_LIST_ID():
    return os.getenv("TRELLO_DOING_LIST_ID")


def TRELLO_DONE_LIST_ID():
    return os.getenv("TRELLO_DONE_LIST_ID")


def test_index_page(monkeypatch, client, load_environment_variables):
    monkeypatch.setattr(requests, 'get', stub)
    response = client.get('/')
    assert response.status_code == 200
    assert 'Item Name - Test One' in response.data.decode()


class StubResponse():
    def __init__(self, fake_response_data, status_code=200):
        self.fake_response_data = fake_response_data
        self._status_code = status_code

    def json(self):
        return self.fake_response_data

    @property
    def status_code(self):
        return self._status_code


def stub(url, params={}):
    test_board_id = os.environ.get('TRELLO_BOARD_ID')
    if url == f'https://api.trello.com/1/boards/{test_board_id}/cards':
        mock_data_file_path = find_dotenv('trello_cards_mock_data.json')
        with open(mock_data_file_path, 'r') as file:
            fake_response_data = json.load(file)

        return StubResponse(fake_response_data)
    raise Exception(f'Integration test did not expect URL "{url}"')


def test_view_model_todo_items(load_environment_variables,
                               example_view_model_items):
    assert len(example_view_model_items.todo_items) > 0
    assert all(
        item.status == "To Do" for item in example_view_model_items.todo_items
    )


def test_view_model_doing_items(load_environment_variables,
                                example_view_model_items):
    assert len(example_view_model_items.doing_items) > 0
    assert all(
        item.status == "Doing" for item in example_view_model_items.doing_items
    )


def test_view_model_done_items(load_environment_variables,
                               example_view_model_items):
    assert len(example_view_model_items.done_items) > 0
    assert all(
        item.status == "Done" for item in example_view_model_items.done_items
    )
