import os

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
def example_view_model_items(load_environment_variables):
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
