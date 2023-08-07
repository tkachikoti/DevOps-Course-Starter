"""
This module provides functions to interact with a Trello board for managing a to-do list. It includes the ability to:

- Retrieve all to-do items (cards) from a specified Trello board
- Fetch a specific item by its ID and status
- Add a new item with a specified title to the to-do list on Trello
- Update an existing item on Trello

The module uses the Trello API to perform these actions, and it translates Trello cards into a specific item dictionary format, including the title, ID, and status.

The following constants are used to configure the Trello board, lists, and authentication:
- TRELLO_API_KEY: The API key for Trello
- TRELLO_API_TOKEN: The API token for Trello
- TRELLO_BOARD_ID: The ID of the Trello board to be used
- TRELLO_TODO_LIST_ID: The ID of the to-do list on the Trello board
- TRELLO_DONE_LIST_ID: The ID of the done list on the Trello board
- TRELLO_API_BASE_URL: The base URL for the Trello API

The module requires the requests library and expects the dotenv library to be used for loading environment variables containing the Trello API key and token.
"""


import requests
import os

from dotenv import load_dotenv

load_dotenv()
TRELLO_API_KEY = os.getenv("TRELLO_API_KEY")
TRELLO_API_TOKEN = os.getenv("TRELLO_API_TOKEN")

TRELLO_BOARD_ID = "c1h21Oxp/"
TRELLO_TODO_LIST_ID = "64ce4da9a7308596be1bd091"
TRELLO_DONE_LIST_ID = "64ce4dbc20ab4eb16e1829f8"
TRELLO_API_BASE_URL = "https://api.trello.com/1/"
BOARDS_URL_PATH = "boards/"
CARDS_URL_PATH = "cards/"


def create_base_payload():
    return {"key": TRELLO_API_KEY, "token": TRELLO_API_TOKEN}

def translate_trello_card_to_item(trello_card):
    """
    Translates a Trello card to an item dictionary as per the old structure.

    Args:
        trello_card (dict): The Trello card data.

    Returns:
        dict: The translated item.
    """

    # Extract the required fields from the Trello card
    title = trello_card.get('name')
    id = trello_card.get('id')
    id_list = trello_card.get('idList')

    # Determine the status based on the list ID
    status = 'Not Started' if id_list == TRELLO_TODO_LIST_ID else 'Done'

    # Construct and return the item dictionary
    item = {
        'id': id,
        'title': title,
        'status': status
    }
    return item

def get_items():
    """
    Fetch all to-do items (cards) for the specified board.

    Returns:
        list: The list of items from board.
    """
    # Prepare the payload with the Trello API key and token
    payload = create_base_payload()
    r = requests.get(TRELLO_API_BASE_URL + BOARDS_URL_PATH + TRELLO_BOARD_ID + CARDS_URL_PATH[:-1], params=payload)

    # Check if the request was successful and the response contains JSON data
    if r.status_code == requests.codes.ok and r.json():
        trello_cards = r.json()
        items = [translate_trello_card_to_item(card) for card in trello_cards]
    else:
        # Return an empty list if the response is unsuccessful or contains no data
        items = []
        
    return items

def get_item(id, status):
    """
    Fetches the saved item (card) with the specified ID from specified board.

    Args:
        id: The ID of the item.
        status: The status of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    # Prepare the payload with the Trello API key and token
    payload = create_base_payload()
    r = requests.get(TRELLO_API_BASE_URL + CARDS_URL_PATH + id, params=payload)
    
    # Check if the request was successful and the response contains JSON data
    if r.status_code == requests.codes.ok and r.json():
        trello_card = r.json()
        item = translate_trello_card_to_item(trello_card)
    else:
        # Return None if the response is unsuccessful or contains no data
        item = None

    return item

def add_item(title):
    """
    Adds a new item (card) with the specified title to the to-do list.

    Returns:
        item: Saved item.
    """
    # Prepare the payload with the Trello API key and token
    payload = create_base_payload()
    payload['idList'] = TRELLO_TODO_LIST_ID
    payload['name'] = title
    r = requests.post(TRELLO_API_BASE_URL + CARDS_URL_PATH[:-1], params=payload)
    
    # Check if the request was successful and the response contains JSON data
    if r.status_code == requests.codes.ok and r.json():
        trello_card = r.json()
        item = translate_trello_card_to_item(trello_card)
    else:
        # Return None if the response is unsuccessful or contains no data
        item = None

    return item

def save_item(item):
    """
    Updates an existing item (card). If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.

    Returns:
        dict: The updated item, or None if the update was unsuccessful.
    """

    # Prepare the payload with the Trello API key and token
    payload = create_base_payload()

    # Update the name (title) of the card
    payload['name'] = item['title']

    # Determine the list ID based on the item's status
    payload['idList'] = TRELLO_TODO_LIST_ID if item['status'] == 'Not Started' else TRELLO_DONE_LIST_ID

    # Send the PUT request to update the card
    r = requests.put(TRELLO_API_BASE_URL + CARDS_URL_PATH + item['id'], params=payload)

    # Check if the request was successful and the response contains JSON data
    if r.status_code == requests.codes.ok and r.json():
        trello_card = r.json()
        updated_item = translate_trello_card_to_item(trello_card)
    else:
        # Return None if the response is unsuccessful or contains no data
        updated_item = None

    return updated_item

if __name__ == '__main__':
    #get_items()
    #get_item('64cfcab076d02235dff342d5', 'Not Started')
    #add_item('Test item')