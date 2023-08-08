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
- TRELLO_API_BASE_URL: The base URL for the Trello API

The module requires the requests library and expects the dotenv library to be used for loading environment variables containing the Trello API key and token.
"""


import requests
import os

from dotenv import load_dotenv

from todo_app.data.item import Item

load_dotenv()
TRELLO_API_KEY = os.getenv("TRELLO_API_KEY")
TRELLO_API_TOKEN = os.getenv("TRELLO_API_TOKEN")
TRELLO_BOARD_ID = os.getenv("TRELLO_BOARD_ID")

TRELLO_API_BASE_URL = "https://api.trello.com/1/"
BOARDS_URL_PATH = "boards/"
CARDS_URL_PATH = "cards/"


def create_base_payload():
    return {"key": TRELLO_API_KEY, "token": TRELLO_API_TOKEN}


def get_items():
    """
    Fetch all to-do items (cards) for the specified board.

    Returns:
        list: The list of items from board.
    """
    # Prepare the payload with the Trello API key and token
    payload = create_base_payload()
    r = requests.get(TRELLO_API_BASE_URL + BOARDS_URL_PATH + TRELLO_BOARD_ID + '/' + CARDS_URL_PATH[:-1], params=payload)

    # Check if the request was successful and the response contains JSON data
    if r.status_code == requests.codes.ok and r.json():
        trello_cards = r.json()
        items = [Item.translate_trello_card_to_item(card) for card in trello_cards]
    else:
        # Return an empty list if the response is unsuccessful or contains no data
        items = []

    return items


def get_item(id):
    """
    Fetches the saved item (card) with the specified ID from specified board.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    # Prepare the payload with the Trello API key and token
    payload = create_base_payload()
    r = requests.get(TRELLO_API_BASE_URL + CARDS_URL_PATH + id, params=payload)

    # Check if the request was successful and the response contains JSON data
    if r.status_code == requests.codes.ok and r.json():
        trello_card = r.json()
        item = Item.translate_trello_card_to_item(trello_card)
    else:
        # Return None if the response is unsuccessful or contains no data
        item = None

    return item


def add_item(item):
    """
    Adds a new item (card) with the specified title to the to-do list.

    Returns:
        item: Saved item.
    """
    # Prepare the payload with the Trello API key and token
    payload = create_base_payload()
    payload['idList'] = item.get_id_list()
    payload['name'] = item.get_title()
    payload['desc'] = item.get_description()
    payload['due'] = item.get_due_date()
    r = requests.post(TRELLO_API_BASE_URL + CARDS_URL_PATH[:-1],
                      params=payload)

    # Check if the request was successful and the response contains JSON data
    if r.status_code == requests.codes.ok and r.json():
        trello_card = r.json()
        item = Item.translate_trello_card_to_item(trello_card)
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

    # Update card
    payload['name'] = item.get_title()
    payload['idList'] = item.get_id_list()

    # Send the PUT request to update the card
    r = requests.put(TRELLO_API_BASE_URL + CARDS_URL_PATH + item.get_id(), params=payload)

    # Check if the request was successful and the response contains JSON data
    if r.status_code == requests.codes.ok and r.json():
        trello_card = r.json()
        updated_item = Item.translate_trello_card_to_item(trello_card)
    else:
        # Return None if the response is unsuccessful or contains no data
        updated_item = None

    return updated_item


def delete_item(id):
    """
    Deletes an existing item (card) with the specified ID from the Trello
    board.

    Args:
        id: The ID of the item to delete.

    Returns:
        bool: True if the deletion was successful, False otherwise.
    """

    # Prepare the payload with the Trello API key and token
    payload = create_base_payload()

    # Send the DELETE request to remove the card
    r = requests.delete(TRELLO_API_BASE_URL + CARDS_URL_PATH + id,
                        params=payload)

    # Check if the request was successful (status code 200)
    if r.status_code == requests.codes.ok:
        return True
    else:
        return False
