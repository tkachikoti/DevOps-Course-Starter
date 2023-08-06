import requests
import os

from dotenv import load_dotenv

load_dotenv()
TRELLO_API_KEY = os.getenv('TRELLO_API_KEY')
TRELLO_API_TOKEN = os.getenv('TRELLO_API_TOKEN')
TRELLO_BOARD_ID = os.getenv('TRELLO_BOARD_ID')

TRELLO_TODO_LIST_ID = '64ce4da9a7308596be1bd091'
TRELLO_DONE_LIST_ID = '64ce4dbc20ab4eb16e1829f8'
TRELLO_API_BASE_URL = 'https://api.trello.com/1/'
TRELLO_API_BOARDS_URL = TRELLO_API_BASE_URL + 'boards/' + TRELLO_BOARD_ID + '/'

def get_items():
    """
    Fetch all to-do items (cards) for the specified board.

    Returns:
        list: The list of items from board.
    """

    payload = {'key': TRELLO_API_KEY, 'token': TRELLO_API_TOKEN}
    r = requests.get(TRELLO_API_BOARDS_URL + 'cards', params=payload)
    print(r.url)
    print(r.json())

    #return session.get('items', _DEFAULT_ITEMS.copy())

def add_item(title):
    """
    Adds a new item (card) with the specified title to the to-do list on a specified board.

    Returns:
        item: Saved item.
    """

    payload = {'key': TRELLO_API_KEY, 'token': TRELLO_API_TOKEN}
    r = requests.get(TRELLO_API_BOARDS_URL + 'cards', params=payload)
    print(r.url)
    print(r.json())

    #return session.get('items', _DEFAULT_ITEMS.copy())

if __name__ == '__main__':
    get_items()