import sys
from PySide2.QtWidgets import (QLabel, QProgressBar, QDialog, QHBoxLayout, QWidget, QVBoxLayout)
from PySide2.QtCore import Signal
from time import sleep

class progress_bar(QWidget):
    set_progress = Signal(int, int, int)

    def __init__(self):
        super().__init__()

        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self._progress_bar = QProgressBar(self)
        self._progress_bar.setMaximum(100)
        self._progress_bar.setGeometry(0, 0, 300, 25)
        self._progress_bar.setValue(0)
        self._layout.addWidget(self._progress_bar)

        self._time_wrapper = QHBoxLayout()
        self._time_expired_label = QLabel("")
        self._time_left_label = QLabel("")
        self._time_wrapper.addWidget(self._time_expired_label)
        self._time_wrapper.addWidget(self._time_left_label)
        self._layout.addLayout(self._time_wrapper)

        self.resize(500, 80)

        self.set_progress.connect(self._set_progress)

    def _set_progress(self, percentage_done, time_elapsed, time_remaining):
        self._progress_bar.setValue(percentage_done)
        self._time_expired_label.setText("Time elapsed: " + time_elapsed.__str__() + "s")
        self._time_left_label.setText("Time remaining: " + time_remaining.__str__() + "s")

    def close_with_delay(self):
        sleep(0.8)
        self.close()
