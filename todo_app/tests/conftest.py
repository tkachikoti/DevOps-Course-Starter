import os
from time import sleep
import pytest
from dotenv import find_dotenv, load_dotenv

from todo_app.data.view_model import ViewModel
from todo_app.data.item import Item
from todo_app import app


TIME_IN_SECONDS = 1


@pytest.fixture
def load_fake_environment_variables():
    # Use our test integration config instead of the 'real' version
    os.environ["USE_MOCK_MONGO"] = "True"
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)


@pytest.fixture
def client(load_fake_environment_variables):
    # Create the new app.
    test_app = app.create_app()
    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        # Give the app a moment to start
        sleep(TIME_IN_SECONDS)

        yield client


@pytest.fixture
def example_view_model_items(load_fake_environment_variables):
    items_data = [
        {"title": f"Task {i}", "id_list": list_name}
        for i, list_name in enumerate(["TODO_LIST", "DOING_LIST", "DONE_LIST"] * 2, start=1)
    ]

    items = [Item(data) for data in items_data]
    return ViewModel(items)
