"""
This module provides functions to interact with a MongoDB for managing a
to-do list. It includes the ability to:

- Retrieve all to-do items from a specified collection
- Fetch a specific item by its ID and status
- Add a new item with a specified title to a collection
- Update an existing item in a collection by its ID

"""


import logging
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId

from todo_app.data.item import Item
from flask import current_app

logger = logging.getLogger(__name__)


def get_items():
    """
    Fetch all items from tasks collection.

    Returns:
        list: The list of items, or raises an exception if the
        request is unsuccessful.
    """
    try:
        retrieved_items = current_app.mongo_db_manager.list_documents(
            "TASKS_COLLECTION"
        )
        processed_items = []
        for item in retrieved_items:
            processed_items.append(Item(item))
        return processed_items
    except PyMongoError as e:
        # Handle MongoDB errors
        logger.error("An error occurred while fetching items from Tasks Collection: ", e)
        raise


def get_item(id):
    """
    Fetches the saved item with the specified ID from tasks collection.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or raises an exception if the item is not found.
    """
    try:
        document_id = ObjectId(id)
        item = current_app.mongo_db_manager.find_document(
            "TASKS_COLLECTION", {"_id": document_id}
        )
        return Item(item)
    except PyMongoError as e:
        # Handle MongoDB errors
        logger.error(
            "An error occurred while fetching item from Tasks Collection: ", e
        )
        raise


def add_item(item):
    """
    Adds a new item with the specified title to the to-do list.

    Returns:
        item: Saved item, or raises an exception if the item is not saved.
    """
    try:
        new_item_id = current_app.mongo_db_manager.insert_document(
            "TASKS_COLLECTION", item.to_dict()
        )
        item.id = new_item_id
        return item
    except PyMongoError as e:
        # Handle MongoDB errors
        logger.error("An error occurred while saving item to Tasks Collection: ", e)
        raise


def save_item(item):
    """
    Updates an existing item. If no existing item matches the ID
    of the specified item, nothing is saved.

    Args:
        item: The item to save.

    Returns:
        dict: The updated item, or raises an exception if the item is not
        updated.
    """

    try:
        # Update item
        document_id = ObjectId(item.id)
        update_result = current_app.mongo_db_manager.update_document(
            "TASKS_COLLECTION", {"_id": document_id}, item.to_dict()
        )

        if update_result.matched_count == 0:
            raise ValueError("Item not found")

        updated_item_data = current_app.mongo_db_manager.find_document(
            "TASKS_COLLECTION", document_id
        )
        return Item(updated_item_data)
    except PyMongoError as e:
        # Handle MongoDB errors
        logger.error(
            "An error occurred while updating item in Tasks Collection: ", e
        )
        raise


def delete_item(id):
    """
    Deletes an existing item with the specified ID from Tasks Collection.

    Args:
        id: The ID of the item to delete.

    Returns:
        bool: True if the deletion was successful, or raises an exception if
        the deletion is unsuccessful.
    """

    try:
        document_id = ObjectId(id)
        current_app.mongo_db_manager.delete_document(
            "TASKS_COLLECTION", {"_id": document_id}
        )
        return True
    except PyMongoError as e:
        # Handle MongoDB errors
        logger.error(
            "An error occurred while deleting item from Tasks Collection: ", e
        )
        raise
