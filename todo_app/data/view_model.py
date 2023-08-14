class ViewModel:
    def __init__(self, items):
        self._items = items

    @property
    def items(self):
        return self._items

    @property
    def todo_items(self):
        return self.filter_items_by_status('To Do')

    @property
    def doing_items(self):
        return self.filter_items_by_status('Doing')

    @property
    def done_items(self):
        return self.filter_items_by_status('Done')

    def filter_items_by_status(self, select_status):
        return [item for item in self.items if item.status == select_status]
