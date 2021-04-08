from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLayout, QScrollArea, QWidgetItem
from PySide6.QtCore import Qt

from gui.OrderableListItem import OrderableListItem


class OrderableListWidget(QScrollArea):
    """All available items in this list"""
    _item_list: list[OrderableListItem]
    """This lists actual widget"""
    _widget: QWidget
    """The widgets layout"""
    _layout: QLayout
    """Decides which way this list is ordered; 1 for ascending, -1 for descending"""
    _order_factor: int

    def __init__(self, order_asc=True, orientation_horizontal=False):
        """Init gui
        :type order_asc: bool
        :param order_asc: Whether to order the list ascending
        :type orientation_horizontal: bool
        :param orientation_horizontal: Should the list orientation be horizontal?
        """
        super().__init__()
        if order_asc:
            self._order_factor = 1
        else:
            self._order_factor = -1
        self._widget = QWidget()
        self.setWidget(self._widget)
        self.setWidgetResizable(True)
        # Set layout
        if orientation_horizontal:
            self._layout = QHBoxLayout()
        else:
            self._layout = QVBoxLayout()
        self._widget.setLayout(self._layout)
        self._layout.setAlignment(Qt.AlignTop)
        self._item_list = []

    def _get_order(self, list_item_a, list_item_b):
        """Defines this lists widget order
        :type list_item_a: OrderableListItem
        :param list_item_a: The first item to compare
        :type list_item_b: OrderableListItem
        :param list_item_b: The second item to compare
        :returns -1|0|1: list_item_a is: before, same, after list_item_b"""
        str_a: str = list_item_a.get_order_string()
        str_b: str = list_item_b.get_order_string()

        if str_a == str_b:
            return 0
        elif str_a < str_b:
            return -1 * self._order_factor
        else:
            return 1 * self._order_factor

    def add(self, list_item):
        """Add a new item to the list
        :type list_item: OrderableListItem
        :param list_item: The item to add
        """
        # Subscribe to changes
        list_item.subscribe(OrderableListItem.DELETED, self._item_deleted)
        list_item.subscribe(OrderableListItem.UPDATED, self._item_updated)
        # Make sure to add the item only once
        if list_item not in self._item_list:
            list_item_inserted = False
            self._item_list.append(list_item)

            # Walk all existing items
            for i in range(self._layout.count()):
                existing_item: OrderableListItem = self._layout.itemAt(i).widget()

                if 1 == self._get_order(existing_item, list_item):
                    self._layout.insertWidget(i, list_item)
                    list_item_inserted = True
                    break
            if not list_item_inserted:
                self._layout.addWidget(list_item)

    def _item_deleted(self, item):
        """Delete an item from the list
        :type item: OrderableListItem
        :param item: The item to delete
        """
        # See if the item exists in this list
        try:
            i: int = self._item_list.index(item)
        except ValueError:
            return
        # Delete the item
        self._item_list.pop(i)

    def _item_updated(self, item):
        """Update the list with the items new information
        :type item: OrderableListItem
        :param item: The item that was updated
        """
        pass
