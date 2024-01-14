"""
Item Class

This class represents a to-do item, with attributes for its ID, title, and
status. The status can be 'Not Started' or 'Complete'. The class provides
methods to mark the item as complete or not started, and update the title.
"""


class Item:
    def __init__(self, item_data):
        """Initialize a new Item with the given ID, title, and status."""
        self._id = item_data.get('_id', None)
        self._title = item_data.get('title')
        self._id_list = item_data.get('id_list', "TODO_LIST")
        self._description = item_data.get('description', None)
        self._due_date = item_data.get('due_date', None)

    @property
    def id(self):
        """
        Returns the id of the item.

        Returns:
            str: The id of the item.
        """
        return self._id

    @id.setter
    def id(self, new_id):
        """Update the due date of the item."""
        self._id = new_id

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
            'To Do' if self.id_list == "TODO_LIST"
            else 'Doing' if self.id_list == "DOING_LIST"
            else 'Done'
        )

    def to_dict(self):
        """
        Convert the item properties to a dictionary.

        Returns:
            dict: A dictionary representation of the item.
        """
        return {
            "title": self._title,
            "id_list": self._id_list,
            "description": self._description,
            "due_date": self._due_date
        }

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
        self._id_list = "TODO_LIST"

    def mark_as_doing(self):
        """Mark the item as not started."""
        self._id_list = "DOING_LIST"

    def mark_as_done(self):
        """Mark the item as complete."""
        self._id_list = "DONE_LIST"

    def __str__(self):
        """Return a string representation of the item."""
        return (
            f"Item(title={self.title}, id={self.id}, id_list={self.id_list}, "
            f"description={self.description}, due_date={self.due_date})"
        )
