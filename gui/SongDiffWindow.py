import webbrowser
from typing import List
from functools import partial
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QMessageBox, QScrollArea, QGridLayout, QLabel,\
    QPushButton
import xml.etree.ElementTree as Xml
from difflib import HtmlDiff
import re

from Song import Song


class SongDiffWindow(QMainWindow):
    def __init__(self, song_orig, song_similar):
        """Displays the difference between two songs
        :type song_orig: Song.Song
        :param song_orig: The original song
        :type song_similar: Song.Song
        :param song_similar: The similar song
        """
        super().__init__()
        self._song_orig = song_orig
        self._song_similar = song_similar

        # Setup gui
        self.resize(800, 550)
        self.setWindowTitle(self._song_orig.get_name() + ' - Similar Songs')

        self.scrollableWrapper: QScrollArea = QScrollArea()
        self.setCentralWidget(self.scrollableWrapper)

        self.centralLayout: QGridLayout = QGridLayout()
        self.centralLayout.setColumnStretch(0, 1)
        self.centralLayout.setColumnStretch(1, 30)
        self.centralLayout.setColumnStretch(2, 1)
        self.centralLayout.setColumnStretch(3, 30)

        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.centralLayout)

        self.scrollableWrapper.setWidget(self.centralWidget)
        self.scrollableWrapper.setWidgetResizable(True)

        # Show diff
        self._show_diff()

    def _show_diff(self):
        """Calculate the diff between the two songs
        :return: list[str]"""
        song_orig_line_str_list: List[str] = [str(line) for line in self._song_orig.get_line_list()]
        song_similar_line_str_list: List[str] = [str(line) for line in self._song_similar.get_line_list()]

        # Compare
        html_diff: HtmlDiff = HtmlDiff()
        html_diff._file_template = "<table>%(table)s</table>"
        html_diff._table_template = "%(data_rows)s"
        diff_file: str = html_diff.make_file(song_orig_line_str_list, song_similar_line_str_list)

        # Add column header
        col_num: int
        for col_num in (1, 3):
            header_text: str
            # Original song
            if 1 == col_num:
                header_text = self._song_orig.get_name()
            # Similar song
            else:
                header_text = self._song_similar.get_name()
            label: QLabel = QLabel(header_text)
            label.setStyleSheet('font-weight: bold')
            self.centralLayout.addWidget(label, 0, col_num)
            # Subscribe to changes
            if 1 == col_num:
                self._song_updated(label, self._song_orig)
                self._song_orig.subscribe(Song.UPDATED, partial(self._song_updated, label))
            else:
                self._song_updated(label, self._song_similar)
                self._song_similar.subscribe(Song.UPDATED, partial(self._song_updated, label))

        # Prepare for xml parse
        diff_file = diff_file.replace('&nbsp;', ' '). \
            replace('<span class="diff_sub">', '{diff sub}'). \
            replace('<span class="diff_chg">', '{diff chg}'). \
            replace('<span class="diff_add">', '{diff add}'). \
            replace('</span>', '{/diff}')

        # Parse diff file
        tree: Xml = Xml.fromstring(diff_file)
        row_count: int = 0
        row: Xml.Element

        for row in tree:
            row_count += 1
            cell_count = 0
            cell: Xml.Element

            # Create the actual diff
            for cell in row:
                cell_count += 1
                column_start: int
                # Original
                if 3 >= cell_count:
                    column_start = 0
                # Similarity
                else:
                    column_start = 2

                # Parse cell type
                if 'class' not in cell.attrib.keys():
                    # Text
                    cell_widget = self._parse_xml_cell(cell.text)
                    self.centralLayout.addWidget(cell_widget, row_count, column_start + 1)
                elif 'diff_next' == cell.attrib['class']:
                    # Link to next edited line
                    # Not shown in view
                    pass
                elif 'diff_header' == cell.attrib['class']:
                    # Line number
                    self.centralLayout.addWidget(QLabel(cell.text), row_count, column_start)
                else:
                    raise KeyError('Unknown element type')
        # Add footer
        row_count += 1
        for col_num in (1, 3):
            song: Song
            # Original song
            if 1 == col_num:
                song = self._song_orig
            # Similar song
            else:
                song = self._song_similar
            # Keep
            button_keep: QPushButton = QPushButton('Keep "' + song.get_name() + '"')
            button_keep.clicked.connect(partial(self._keep_song, song))
            self.centralLayout.addWidget(button_keep, row_count + 0, col_num)
            # Delete
            button_delete: QPushButton = QPushButton('Delete "' + song.get_name() + '"')
            button_delete.clicked.connect(partial(self._delete_song, song))
            self.centralLayout.addWidget(button_delete, row_count + 1, col_num)
            # Edit
            button_edit: QPushButton = QPushButton('Edit "' + song.get_name() + '"')
            button_edit.clicked.connect(partial(webbrowser.open, str(song)))
            self.centralLayout.addWidget(button_edit, row_count + 2, col_num)

    @staticmethod
    def _song_updated(label, song):
        """The given song was updated
        :type label: QLabel
        :param label: The label associated with this song
        :type song: Song
        :param song: The song that changed"""
        if song.is_marked_for_keeping():
            label.setStyleSheet('background-color: green')
        elif song.is_marked_for_deleting():
            label.setStyleSheet('background-color: red')

    @staticmethod
    def _keep_song(song):
        """Mark the given song to keep
        :type song: Song
        :param song: The song to mark"""
        song.mark_for_keeping()

    @staticmethod
    def _delete_song(song):
        """Mark the given song for deleting
        :type song: Song
        :param song: The song to mark"""
        song.mark_for_deleting()

    @staticmethod
    def _parse_xml_cell(text):
        """Convert a cells text into a gui element
        :type text: str
        :param text: The cells text to parse
        :return QWidget: The parsed cell
        """
        return_widget = QWidget()
        if None is text:
            return return_widget
        # Parse text
        text_as_list: List[tuple[str, str]] = SongDiffWindow.__extract_diff_tag(text)
        # Convert to gui
        layout: QHBoxLayout = QHBoxLayout(return_widget)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        for part in text_as_list:
            if 'default' == part[0]:
                change_widget = QLabel(part[1])
                layout.addWidget(change_widget)
            elif 'sub' == part[0]:
                change_widget = QLabel(part[1])
                change_widget.setStyleSheet('background-color: red')
                layout.addWidget(change_widget)
            elif 'chg' == part[0]:
                change_widget = QLabel(part[1])
                change_widget.setStyleSheet('background-color: orange')
                layout.addWidget(change_widget)
            elif 'add' == part[0]:
                change_widget = QLabel(part[1])
                change_widget.setStyleSheet('background-color: green')
                layout.addWidget(change_widget)
            else:
                raise KeyError('Unknown change key')
        layout.addStretch()
        return return_widget

    @staticmethod
    def __extract_diff_tag(string):
        """Extract the diff tags from a string
        :type string: str
        :param string: The string to parse
        :return list[tuple[str, str]]: Extracted parts of the string"""
        return_list = []
        regex_string = r"(?P<prefix>[^{]*){diff ?(?P<diff_type>[^}]*)}(?P<diff_content>[^{]*){\/diff}(?P<postfix>[^{]*)"
        matches = re.finditer(regex_string, string)
        match_count = 0
        for match in matches:
            match_count += 1
            # Prefix
            if '' != match.group('prefix'):
                return_list.append(('default', match.group('prefix')))
            # Diff
            if '' != match.group('diff_content'):
                diff_type: str
                if '' == match.group('diff_type'):
                    diff_type = 'default'
                else:
                    diff_type = match.group('diff_type')
                return_list.append((diff_type, match.group('diff_content')))
            # Postfix
            if '' != match.group('postfix'):
                return_list.append(('default', match.group('postfix')))
        # No match found
        if 1 > match_count:
            return [('default', string)]
        else:
            return return_list


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    # Open the main window
    from pathlib import Path

    song_diff: SongDiffWindow = SongDiffWindow(Song(Path("D:\\Git\\SongBeamer_SimilarSongFinder\\Songs\\95 Krasse Thesen.sng")),
                                               Song(Path("D:\\Git\\SongBeamer_SimilarSongFinder\\Songs\\99 Luftballons.sng")))
    song_diff.show()
    # Quit when the user exits the program
    sys.exit(app.exec_())
