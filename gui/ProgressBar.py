from PySide2.QtWidgets import (QLabel, QProgressBar, QHBoxLayout, QWidget, QVBoxLayout)
from PySide2.QtCore import Signal
from time import sleep


class ProgressBar(QWidget):
    # Incoming progress updates
    set_progress = Signal(int, int, int)

    def __init__(self):
        """Opens a progress bar widget"""
        super().__init__()
        # General layout
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)
        # The progress bar itself
        self._progress_bar = QProgressBar(self)
        self._progress_bar.setMaximum(100)
        self._progress_bar.setGeometry(0, 0, 300, 25)
        self._progress_bar.setValue(0)
        self._layout.addWidget(self._progress_bar)
        # Setup time display
        self._time_wrapper = QHBoxLayout()
        self._time_expired_label = QLabel("")
        self._time_left_label = QLabel("")
        self._time_wrapper.addWidget(self._time_expired_label)
        self._time_wrapper.addWidget(self._time_left_label)
        self._layout.addLayout(self._time_wrapper)
        # Set Size
        self.resize(500, 80)
        # Register progress update handler
        # noinspection PyUnresolvedReferences
        self.set_progress.connect(self._set_progress)

    def _set_progress(self, percentage_done: int, time_elapsed: int, time_remaining: int):
        """Handle incoming progress updates
        :param percentage_done: The progress to set, from 0 to 100
        :param time_elapsed: Total time elapsed, in seconds
        :param time_remaining: Approximate time remaining, in seconds
        """
        self._progress_bar.setValue(percentage_done)
        self._time_expired_label.setText("Time elapsed: " + str(time_elapsed) + "s")
        self._time_left_label.setText("Time remaining: " + str(time_remaining) + "s")

    def close_with_delay(self):
        """Close the progress bar widget with a short delay"""
        sleep(0.8)
        self.close()
