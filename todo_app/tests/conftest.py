import os
from time import sleep
from threading import Thread

import pytest
from dotenv import find_dotenv, load_dotenv
from selenium import webdriver

from todo_app.data.trello_items import create_board, delete_board
from todo_app.data.view_model import ViewModel
from todo_app.data.item import Item
from todo_app import app

TIME_IN_SECONDS = 1


@pytest.fixture
def load_fake_environment_variables():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)


@pytest.fixture
def load_real_environment_variables():
    # Load the real environment variables
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)


@pytest.fixture
def client(load_fake_environment_variables):
    # Create the new app.
    test_app = app.create_app()
    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client


@pytest.fixture
def example_view_model_items(load_fake_environment_variables):
    # Create mock items
    item1 = Item(title="Task 1", id_list=os.getenv("TRELLO_TODO_LIST_ID"))
    item2 = Item(title="Task 2", id_list=os.getenv("TRELLO_DOING_LIST_ID"))
    item3 = Item(title="Task 3", id_list=os.getenv("TRELLO_DONE_LIST_ID"))
    item4 = Item(title="Task 4", id_list=os.getenv("TRELLO_TODO_LIST_ID"))
    item5 = Item(title="Task 5", id_list=os.getenv("TRELLO_DOING_LIST_ID"))
    item6 = Item(title="Task 6", id_list=os.getenv("TRELLO_DONE_LIST_ID"))

    return ViewModel([item1, item2, item3, item4, item5, item6])


@pytest.fixture(scope='module')
def app_with_temp_board(load_real_environment_variables):
    # Create the new board & update the board id environment variable
    temp_board = create_board("Temp Board For Testing")
    os.environ['TRELLO_BOARD_ID'] = temp_board["id"]

    # Construct the new application
    application = app.create_app()

    # Start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()

    # Give the app a moment to start
    sleep(TIME_IN_SECONDS)

    yield application

    # Tear Down
    thread.join(1)
    delete_board(temp_board["id"])


@pytest.fixture(scope="module")
def driver():
    with webdriver.Firefox() as driver:
        yield driver
