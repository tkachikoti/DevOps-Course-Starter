"""
Item Class

This class represents a to-do item, with attributes for its ID, title, and
status. The status can be 'Not Started' or 'Complete'. The class provides
methods to mark the item as complete or not started, and update the title.

The following constants are used to configure the Trello lists:
- TRELLO_TODO_LIST_ID: The ID of the 'To Do' list on the Trello board
- TRELLO_DOING_LIST_ID: The ID of the 'Doing' list on the Trello board
- TRELLO_DONE_LIST_ID: The ID of the 'Done' list on the Trello board
"""

import os


def TRELLO_TODO_LIST_ID():
    return os.getenv("TRELLO_TODO_LIST_ID")


def TRELLO_DOING_LIST_ID():
    return os.getenv("TRELLO_DOING_LIST_ID")


def TRELLO_DONE_LIST_ID():
    return os.getenv("TRELLO_DONE_LIST_ID")


class Item:
    def __init__(self, title, id=None, id_list=TRELLO_TODO_LIST_ID(),
                 description=None, due_date=None):
        """Initialize a new Item with the given ID, title, and status."""
        self._title = title
        self._id = id
        self._id_list = id_list
        self._description = description
        self._due_date = due_date

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

        return cls(title, id, id_list, description, due_date)

    @property
    def id(self):
        """
        Returns the id of the item.

        Returns:
            str: The id of the item.
        """
        return self._id

    @property
    def id_list(self):
        """
        Returns the list id that the item belongs to.

        Returns:
            str: The id of the item's list.
        """
        return self._id_list

    @property
    def description(self):
        """
        Returns the item description.

        Returns:
            str: The description of the item.
        """
        return self._description

    @description.setter
    def description(self, new_description):
        """Update the description of the item."""
        self._description = new_description

    @property
    def due_date(self):
        """
        Returns the item due date.

        Returns:
            str: The due date of the item.
        """
        return self._due_date

    @due_date.setter
    def due_date(self, new_due_date):
        """Update the due date of the item."""
        self._due_date = new_due_date

    @property
    def title(self):
        """
        Returns the title of the item.

        Returns:
            str: The title of the item.
        """
        return self._title

    @title.setter
    def title(self, new_title):
        """Update the title of the item with the new title."""
        self._title = new_title

    @property
    def status(self):
        """
        Determine status based on the list ID and returns the status of
        the item.

        Returns:
            str: The status of the item.
        """
        return (
            'To Do' if self.id_list == TRELLO_TODO_LIST_ID()
            else 'Doing' if self.id_list == TRELLO_DOING_LIST_ID()
            else 'Done'
        )

    def is_status_todo(self):
        """Check if the item is marked as "To Do".

        Returns:
            bool: True if the item is "To Do", False otherwise.
        """
        return self.status == 'To Do'

    def is_status_doing(self):
        """Check if the item is marked as "Doing".

        Returns:
            bool: True if the item is "Doing", False otherwise.
        """
        return self.status == 'Doing'

    def is_status_done(self):
        """Check if the item is marked as "Done".

        Returns:
            bool: True if the item is "Done", False otherwise.
        """
        return self.status == 'Done'

    def mark_as_to_do(self):
        """Mark the item as to do."""
        self._id_list = TRELLO_TODO_LIST_ID()

    def mark_as_doing(self):
        """Mark the item as not started."""
        self._id_list = TRELLO_DOING_LIST_ID()

    def mark_as_done(self):
        """Mark the item as complete."""
        self._id_list = TRELLO_DONE_LIST_ID()

    def __str__(self):
        """Return a string representation of the item."""
        return (
            f"Item(title={self.title}, id={self.id}, id_list={self.id_list}, "
            f"description={self.description}, due_date={self.due_date})"
        )
