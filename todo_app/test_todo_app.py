import os

import pytest
from dotenv import load_dotenv

from todo_app.data.view_model import ViewModel
from todo_app.data.item import Item


@pytest.fixture
def load_environment_variables():
    load_dotenv()


def TRELLO_TODO_LIST_ID():
    return os.getenv("TRELLO_TODO_LIST_ID")


def TRELLO_DOING_LIST_ID():
    return os.getenv("TRELLO_DOING_LIST_ID")


def TRELLO_DONE_LIST_ID():
    return os.getenv("TRELLO_DONE_LIST_ID")


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
