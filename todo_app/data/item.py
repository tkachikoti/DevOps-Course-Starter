"""
Item Class

This class represents a to-do item, with attributes for its ID, title, and
status. The status can be 'Not Started' or 'Complete'. The class provides
methods to mark the item as complete or not started, and update the title.

The following constants are used to configure the Trello lists:
- TRELLO_NS_LIST_ID: The ID of the to-do list on the Trello board
- TRELLO_COMPLETE_LIST_ID: The ID of the done list on the Trello board
"""

import os


TRELLO_NS_LIST_ID = os.getenv("TRELLO_NS_LIST_ID")
TRELLO_COMPLETE_LIST_ID = os.getenv("TRELLO_COMPLETE_LIST_ID")


class Item:
    def __init__(self, title, id=None, id_list=TRELLO_NS_LIST_ID,
                 description=None, due_date=None, status='Not Started'):
        """Initialize a new Item with the given ID, title, and status."""
        self.title = title
        self.id = id
        self.id_list = id_list
        self.description = description
        self.due_date = due_date
        self.status = status

    @classmethod
    def translate_trello_card_to_item(cls, trello_card):
        """
        Translates a Trello card to an item dictionary as per the old
        structure.

        Args:
            trello_card (dict): The Trello card data.

        Returns:
            dict: The translated item.
        """

        # Extract required fields from the Trello card
        title = trello_card.get('name')
        id = trello_card.get('id')
        id_list = trello_card.get('idList')
        description = trello_card.get('desc')
        due_date = trello_card.get('due')

        # Determine status based on the list ID
        status = 'Not Started' if id_list == TRELLO_NS_LIST_ID else 'Complete'

        return cls(title, id, id_list, description, due_date, status)

    def get_id(self):
        """
        Returns the id of the item.

        Returns:
            str: The id of the item.
        """
        return self.id

    def get_id_list(self):
        """
        Returns the list id that the item belongs to.

        Returns:
            str: The id of the item's list.
        """
        return self.id_list

    def get_description(self):
        """
        Returns the item description.

        Returns:
            str: The description of the item.
        """
        return self.description

    def get_due_date(self):
        """
        Returns the item due date.

        Returns:
            str: The due date of the item.
        """
        return self.due_date

    def get_title(self):
        """
        Returns the title of the item.

        Returns:
            str: The title of the item.
        """
        return self.title

    def get_status(self):
        """
        Returns the status of the item.

        Returns:
            str: The status of the item.
        """
        return self.status

    def is_complete(self):
        """Check if the item is marked as complete.

        Returns:
            bool: True if the item is complete, False otherwise.
        """
        return self.status == 'Complete'

    def mark_as_complete(self):
        """Mark the item as complete."""
        self.status = 'Complete'
        self.id_list = TRELLO_COMPLETE_LIST_ID

    def mark_as_not_started(self):
        """Mark the item as not started."""
        self.status = 'Not Started'
        self.id_list = TRELLO_NS_LIST_ID

    def update_title(self, new_title):
        """Update the title of the item with the new title."""
        self.title = new_title

    def update_description(self, new_description):
        """Update the description of the item."""
        self.title = new_description

    def update_due(self, new_due_date):
        """Update the due date of the item."""
        self.title = new_due_date

    def __str__(self):
        """Return a string representation of the item."""
        return f"Item(id={self.id}, id_list={self.id_list}, title={self.title}, status={self.status})"
