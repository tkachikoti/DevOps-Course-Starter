"""
This module provides functions to interact with a Trello board for managing a
to-do list. It includes the ability to:

- Retrieve all to-do items (cards) from a specified Trello board
- Fetch a specific item by its ID and status
- Add a new item with a specified title to the to-do list on Trello
- Update an existing item on Trello

The module uses the Trello API to perform these actions, and it translates
Trello cards into a specific item dictionary format, including the title,
ID, and status.

The following constants are used to configure the Trello board, lists, and
authentication:
- TRELLO_API_KEY: The API key for Trello
- TRELLO_API_TOKEN: The API token for Trello
- TRELLO_BOARD_ID: The ID of the Trello board to be used
- TRELLO_API_BASE_URL: The base URL for the Trello API
"""


import requests
import os

from todo_app.data.item import Item


def TRELLO_API_KEY():
    return os.getenv("TRELLO_API_KEY")


def TRELLO_API_TOKEN():
    return os.getenv("TRELLO_API_TOKEN")


def TRELLO_BOARD_ID():
    return os.getenv("TRELLO_BOARD_ID")


TRELLO_API_BASE_URL = "https://api.trello.com/1/"
BOARDS_URL_PATH = "boards/"
LISTS_URL_PATH = "lists/"
CARDS_URL_PATH = "cards/"


def create_base_payload():
    return {"key": TRELLO_API_KEY(), "token": TRELLO_API_TOKEN()}


def create_board(board_name):
    """
    Creates a new board on Trello with the specified name.

    Returns:
        dict: The board that was created, or raises an exception if the board
        is not created.
    """

    # Prepare the payload with the Trello API key and token
    payload = create_base_payload()
    payload['name'] = board_name
    payload['defaultLists'] = "false"

    # Send the POST request to create the board
    url = TRELLO_API_BASE_URL + BOARDS_URL_PATH
    r = requests.post(url, params=payload)

    # Check if the request was successful and the response contains JSON data
    if r.status_code == requests.codes.ok and r.json():
        trello_board = r.json()
    else:
        # Raise an exception if the response is unsuccessful
        r.raise_for_status()

    return trello_board


def delete_board(id):
    """
    Deletes an existing board with the specified ID from Trello.

    Args:
        id: The ID of the board to delete.

    Returns:
        bool: True if the deletion was successful, or raises an exception if
        the deletion is unsuccessful.
    """

    # Prepare the payload with the Trello API key and token
    payload = create_base_payload()

    # Send the DELETE request to remove the board
    url = TRELLO_API_BASE_URL + BOARDS_URL_PATH + id
    r = requests.delete(url, params=payload)

    # Check if the request was successful (status code 200)
    if r.status_code == requests.codes.ok:
        return True
    else:
        # Raise an exception if the response is unsuccessful
        r.raise_for_status()


def create_list_on_board(list_name, board_id):
    """
    Creates a new list on Trello with the specified name.

    Args:
        list_name: The name of the list to create.
        board_id: The ID of the board on which to create the list.

    Returns:
        dict: The list that was created, or raises an exception if the list
        is not created.
    """

    # Prepare the payload with the Trello API key and token
    payload = create_base_payload()
    payload['name'] = list_name

    # Send the POST request to create the list
    url = (
        TRELLO_API_BASE_URL + BOARDS_URL_PATH + board_id + '/'
        + LISTS_URL_PATH[:-1]
    )
    r = requests.post(url, params=payload)

    # Check if the request was successful and the response contains JSON data
    if r.status_code == requests.codes.ok and r.json():
        trello_list = r.json()
    else:
        # Raise an exception if the response is unsuccessful
        r.raise_for_status()

    return trello_list


def delete_list_on_board(id):
    """
    Deletes an existing list with the specified ID from Trello.

    Args:
        id: The ID of the list to delete.

    Returns:
        bool: True if the deletion was successful, or raises an exception if
        the deletion is unsuccessful.
    """

    # Prepare the payload with the Trello API key and token
    payload = create_base_payload()

    # Send the DELETE request to remove the list
    url = TRELLO_API_BASE_URL + LISTS_URL_PATH + id
    r = requests.delete(url, params=payload)

    # Check if the request was successful (status code 200)
    if r.status_code == requests.codes.ok:
        return True
    else:
        # Raise an exception if the response is unsuccessful
        r.raise_for_status()


def get_items():
    """
    Fetch all to-do items (cards) for the specified board.

    Returns:
        list: The list of items from board, or raises an exception if the
        request is unsuccessful.
    """

    items = []
    # Prepare the payload with the Trello API key and token
    payload = create_base_payload()
    url = (TRELLO_API_BASE_URL + BOARDS_URL_PATH + TRELLO_BOARD_ID() +
           '/' + CARDS_URL_PATH[:-1])
    r = requests.get(url, params=payload)

    # Check if the request was successful and the response contains JSON data
    if r.status_code == requests.codes.ok and r.json():
        trello_cards = r.json()
        items = [
            Item.translate_trello_card_to_item(card) for card in trello_cards
        ]
    else:
        # Raise an exception if the response is unsuccessful
        r.raise_for_status()

    return items


def get_item(id):
    """
    Fetches the saved item (card) with the specified ID from specified board.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or raises an exception if the item is not found.
    """
    # Prepare the payload with the Trello API key and token
    payload = create_base_payload()
    url = TRELLO_API_BASE_URL + CARDS_URL_PATH + id
    r = requests.get(url, params=payload)

    # Check if the request was successful and the response contains JSON data
    if r.status_code == requests.codes.ok and r.json():
        trello_card = r.json()
        item = Item.translate_trello_card_to_item(trello_card)
    else:
        # Raise an exception if the response is unsuccessful
        r.raise_for_status()

    return item


def add_item(item):
    """
    Adds a new item (card) with the specified title to the to-do list.

    Returns:
        item: Saved item, or raises an exception if the item is not saved.
    """
    # Prepare the payload with the Trello API key and token
    payload = create_base_payload()
    payload['idList'] = item.id_list
    payload['name'] = item.title
    payload['desc'] = item.description
    payload['due'] = item.due_date

    url = TRELLO_API_BASE_URL + CARDS_URL_PATH[:-1]
    r = requests.post(url, params=payload)

    # Check if the request was successful and the response contains JSON data
    if r.status_code == requests.codes.ok and r.json():
        trello_card = r.json()
        item = Item.translate_trello_card_to_item(trello_card)
    else:
        # Raise an exception if the response is unsuccessful
        r.raise_for_status()

    return item


def save_item(item):
    """
    Updates an existing item (card). If no existing item matches the ID
    of the specified item, nothing is saved.

    Args:
        item: The item to save.

    Returns:
        dict: The updated item, or raises an exception if the item is not
        updated.
    """

    # Prepare the payload with the Trello API key and token
    payload = create_base_payload()

    # Update card
    payload['name'] = item.title
    payload['idList'] = item.id_list

    # Send the PUT request to update the card
    url = TRELLO_API_BASE_URL + CARDS_URL_PATH + item.id
    r = requests.put(url, params=payload)

    # Check if the request was successful and the response contains JSON data
    if r.status_code == requests.codes.ok and r.json():
        trello_card = r.json()
        updated_item = Item.translate_trello_card_to_item(trello_card)
    else:
        # Raise an exception if the response is unsuccessful
        r.raise_for_status()

    return updated_item


def delete_item(id):
    """
    Deletes an existing item (card) with the specified ID from the Trello
    board.

    Args:
        id: The ID of the item to delete.

    Returns:
        bool: True if the deletion was successful, or raises an exception if
        the deletion is unsuccessful.
    """

    # Prepare the payload with the Trello API key and token
    payload = create_base_payload()

    # Send the DELETE request to remove the card
    url = TRELLO_API_BASE_URL + CARDS_URL_PATH + id
    r = requests.delete(url, params=payload)

    # Check if the request was successful (status code 200)
    if r.status_code == requests.codes.ok:
        return True
    else:
        # Raise an exception if the response is unsuccessful
        r.raise_for_status()
