import sys

from PySide6.QtWidgets import (QApplication)

from gui.SimilaritiesWindow import SimilaritiesWindow


class Main:
    def __init__(self):
        """Show the main application window"""
        app = QApplication(sys.argv)
        # Open the main window
        self._main_window = SimilaritiesWindow()
        self._main_window.show()
        self._main_window.do_show_loaded_songs_gui_action()
        # Quit when the user exits the program
        sys.exit(app.exec_())


if __name__ == "__main__":
    Main()
