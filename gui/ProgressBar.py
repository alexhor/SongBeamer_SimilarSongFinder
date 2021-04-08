import math
import timeit

from PySide2.QtWidgets import (QLabel, QProgressBar, QHBoxLayout, QWidget, QVBoxLayout)
from PySide2.QtCore import Signal
from time import sleep


class ProgressBar(QWidget):
    # Incoming progress updates
    set_progress = Signal(int)

    def __init__(self, show_time=True):
        """Opens a progress bar widget
        :type show_time: bool
        :param show_time: If the time should be shown below the progress bar"""
        super().__init__()
        # Setup parameters
        self._show_time: bool = show_time
        self._timer_start: float = 0

        # General layout
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)
        # The progress bar itself
        self._progress_bar = QProgressBar(self)
        self._progress_bar.setMaximum(100)
        self._progress_bar.setGeometry(0, 0, 350, 25)
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

    def startTimer(self):
        """Start the internal timer"""
        self._timer_start = timeit.default_timer()

    def _set_progress(self, percentage_done):
        """Handle incoming progress updates
        :type percentage_done: int
        :param percentage_done: The progress to set, from 0 to 100
        """
        self._progress_bar.setValue(percentage_done)
        if self._show_time:
            time_elapsed, time_remaining = self._get_progress_times(percentage_done)
            self._time_expired_label.setText("Time elapsed: " + str(time_elapsed) + "s")
            self._time_left_label.setText("Time remaining: " + str(time_remaining) + "s")

    def _get_progress_times(self, percentage_done):
        """Get the elapsed and remaining time
        :type percentage_done: float
        :param percentage_done: How much progress has been made
        :return float, float: Time elapsed, Time remaining"""
        time_elapsed = math.floor(timeit.default_timer() - self._timer_start)
        if 0 == percentage_done:
            percentage_done = 1
        time_remaining = math.floor(time_elapsed / percentage_done) - time_elapsed
        return time_elapsed, time_remaining

    def close_with_delay(self):
        """Close the progress bar widget with a short delay"""
        sleep(0.8)
        self.close()
