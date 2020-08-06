import datetime

class ViewModel:
    def __init__(self, items):
        self._items = items

    @property
    def items(self):
        return self._items

    @property
    def outstanding_items(self):
        return [item for item in self._items if item.status == 'Not Started']
    
    @property
    def pending_items(self):
        return [item for item in self._items if item.status == 'In Progress']

    @property
    def all_done_items(self):
        return [item for item in self._items if item.status == 'Done']

    @property
    def recent_done_items(self):
        return [item for item in self._items if item.status == 'Done' and item.editDatetime.date() == datetime.date.today()]

    @property
    def older_done_items(self):
        return [item for item in self._items if item.status == 'Done' and item.editDatetime.date() < datetime.date.today()]