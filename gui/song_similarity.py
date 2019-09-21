from PySide2.QtWidgets import (QLabel, QPushButton, QHBoxLayout, QWidget)

class song_similarity:
    def __init__(self, song_1, song_2):
        self._song_1 = song_1
        self._song_2 = song_2
        self._similar_line_list = {}
        self.__valid = False

    def addSimilarities(self, line, list_of_similarities):
        for similar_line in list_of_similarities:
            self.addSimilarity(line, similar_line, list_of_similarities[similar_line])

    def addSimilarity(self, line, similar_line, score):
        if (line in self._similar_line_list and self._similar_line_list[line]["similar_line"] == similar_line
            or
            similar_line in self._similar_line_list and self._similar_line_list[similar_line]["similar_line"] == line):
                # this similarity was already added
                return
        # add new similarity
        self._similar_line_list[line] = {}
        self._similar_line_list[line]["similar_line"] = similar_line
        self._similar_line_list[line]["score"] = score

    def __repr__(self):
        return self._song_1 + "\n <<>> \n" + self._song_2

    def get_button_widget(self):
        self._button = QPushButton(self.__str__())
        self._button.clicked.connect(self.button_clicked)
        return self._button

    def button_clicked(self, checked):
        # the preview element has to be passed to generate a preview
        if not self.__valid:
            return

        self._window.clear_text_preview()
        self.show_text_preview()
        self._button.setStyleSheet("background-color: red")

    def show_text_preview(self):
        if not self.__valid:
            return

        # add song titles

        # add each similar line
        for line in self._similar_line_list:
            original_line = line
            similar_line = self._similar_line_list[line]["similar_line"]
            # make sure the original line is from the first song
            if original_line.song != self._song_1:
                original_line = similar_line
                similar_line = line

            # create text widgets
            left = QLabel(original_line.__str__())
            right = QLabel(similar_line.__str__())
            # add the elements to the widget
            layout = QHBoxLayout()
            layout.addWidget(left)
            layout.addWidget(right)
            # add the layout to the text preview
            wrapper = QWidget()
            wrapper.setLayout(layout)
            self._window.add_widget_to_text_preview(wrapper)

        # show the songs whole texts
        for line in self._song_1._song_line_list:
            label = QLabel(line.__str__())
            self._window.add_widget_to_left_song_preview(label)

        for line in self._song_2._song_line_list:
            label = QLabel(line.__str__())
            self._window.add_widget_to_right_song_preview(label)

        
        # show the normal song texts

        """
        left_side = self._window.get_preview_text_element_left()
        right_side = self._window.get_preview_text_element_right()

        for line in self._similar_line_list:
            line_element_left = QLabel(line.__str__())
            left_side.addWidget(line_element_left)

            line_element_right = QLabel(self._similar_line_list[line]["similar_line"].__str__())
            right_side.addWidget(line_element_right)"""

    def set_window(self, window):
        self._window = window
        self.__valid = True
