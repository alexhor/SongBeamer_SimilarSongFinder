import sys

from PySide2.QtWidgets import (QApplication)

from gui.MainWindow import MainWindow


class Main:
    def __init__(self):
        """Show the main application window"""
        app = QApplication(sys.argv)
        # Open the main window
        self._main_window = MainWindow()
        self._main_window.show()
        # Quit when the user exits the program
        sys.exit(app.exec_())


if __name__ == "__main__":
    Main()
