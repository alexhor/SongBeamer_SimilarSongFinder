from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLayout, QScrollArea, QWidgetItem

from gui.OrderableListItem import OrderableListItem


class OrderableListWidget(QScrollArea):
    """All available items in this list"""
    _item_list: list[OrderableListItem]
    """This lists actual widget"""
    _widget: QWidget
    """The widgets layout"""
    _layout: QLayout

    def __init__(self, orientation_horizontal=False):
        """
        Init gui
        :type orientation_horizontal: bool
        :param orientation_horizontal: Should the list orientation be horizontal?
        """
        super().__init__()
        self._widget = QWidget()
        self.setWidget(self._widget)
        self.setWidgetResizable(True)
        # Set layout
        if orientation_horizontal:
            self._layout = QHBoxLayout()
        else:
            self._layout = QVBoxLayout()
        self._widget.setLayout(self._layout)
        self._item_list = []

    def add(self, list_item):
        """Add a new item to the list
        :type list_item: OrderableListItem
        :param list_item: The item to add
        """
        # Subscribe to changes
        list_item.subscribe(OrderableListItem.DELETED, self.delete_item)
        list_item.subscribe(OrderableListItem.CHANGED, self.item_updated)
        # Make sure to add the item only once
        if list_item not in self._item_list:
            self._layout.addWidget(list_item)
            self._item_list.append(list_item)

    def delete_item(self, item):
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
        #layout_item: QWidgetItem = self._layout.takeAt(i)
        #layout_item.widget().deleteLater()

    def item_updated(self, item):
        """Update the list with the items new information
        :type item: OrderableListItem
        :param item: The item that was updated
        """
        pass
