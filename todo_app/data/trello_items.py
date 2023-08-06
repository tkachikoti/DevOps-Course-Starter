import requests
import os

from dotenv import load_dotenv

load_dotenv()
TRELLO_API_KEY = os.getenv('TRELLO_API_KEY')
TRELLO_API_TOKEN = os.getenv('TRELLO_API_TOKEN')

TRELLO_BOARD_ID = 'c1h21Oxp/'
TRELLO_TODO_LIST_ID = '64ce4da9a7308596be1bd091'
TRELLO_DONE_LIST_ID = '64ce4dbc20ab4eb16e1829f8'
TRELLO_API_BASE_URL = 'https://api.trello.com/1/'
BOARDS_URL_PATH = 'boards/'
CARDS_URL_PATH = 'cards/'

def create_base_payload():
    return {'key': TRELLO_API_KEY, 'token': TRELLO_API_TOKEN}

def get_items():
    """
    Fetch all to-do items (cards) for the specified board.

    Returns:
        list: The list of items from board.
    """

    payload = create_base_payload()
    r = requests.get(TRELLO_API_BASE_URL + BOARDS_URL_PATH + TRELLO_BOARD_ID + CARDS_URL_PATH[:-1], params=payload)
    print(r.url)
    print(r.json())

    #return session.get('items', _DEFAULT_ITEMS.copy())

def get_item(id, status):
    """
    Fetches the saved item (card) with the specified ID from specified board.

    Args:
        id: The ID of the item.
        status: The status of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    payload = create_base_payload()
    payload['idList'] = TRELLO_TODO_LIST_ID if status=='Not Started'  else TRELLO_DONE_LIST_ID
    r = requests.get(TRELLO_API_BASE_URL + BOARDS_URL_PATH + TRELLO_BOARD_ID + CARDS_URL_PATH + id, params=payload)
    status_code = r.status_code
    print(r.url)
    print(r.json())

def add_item(title):
    """
    Adds a new item (card) with the specified title to the to-do list.

    Returns:
        item: Saved item.
    """

    payload = create_base_payload()
    payload['idList'] = TRELLO_TODO_LIST_ID
    payload['name'] = title
    r = requests.post(TRELLO_API_BASE_URL + CARDS_URL_PATH[:-1], params=payload)
    print(r.url)
    print(r.json())

    #return session.get('items', _DEFAULT_ITEMS.copy())

def save_item(item):
    """
    Updates an existing item (card). If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.
    """
    payload = create_base_payload()
    payload['idList'] = TRELLO_TODO_LIST_ID
    payload['name'] = title
    r = requests.post(TRELLO_API_BASE_URL + CARDS_URL_PATH[:-1], params=payload)
    print(r.url)
    print(r.json())

if __name__ == '__main__':
    #get_items()
    #get_item('64cfcab076d02235dff342d5', 'Not Started')
    #add_item('Test item')