from PySide2.QtWidgets import (QHBoxLayout, QWidget)


class LoadedSongsOverview(QWidget):
    def __init__(self):
        """Show and modify the list of all loaded songs"""
        QWidget.__init__(self)

        # Main layout
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # Adjust the layouts sizes
        self.adjustSize()
