from typing import List

from PySide2.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QListWidget, QScrollArea, QGridLayout, QLabel
from PySide2.QtCore import Qt
import xml.etree.ElementTree as xml
from difflib import HtmlDiff
import re


class SongDiff(QMainWindow):
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

        # Prepare for xml parse
        diff_file = diff_file.replace('&nbsp;', ' '). \
            replace('<span class="diff_sub">', '{diff sub}'). \
            replace('<span class="diff_chg">', '{diff chg}'). \
            replace('<span class="diff_add">', '{diff add}'). \
            replace('</span>', '{/diff}')

        # Parse diff file
        tree: xml = xml.fromstring(diff_file)
        row_count: int = 0
        column: xml.Element

        for column in tree:
            row_count += 1
            cell_count = 0
            cell: xml.Element

            for cell in column:
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
        text_as_list: List[tuple[str, str]] = SongDiff.__extract_diff_tag(text)
        # Convert to gui
        layout = QHBoxLayout(return_widget)
        layout.setSpacing(0)
        layout.setMargin(0)
        for part in text_as_list:
            if 'default' == part[0]:
                change_widget = QLabel(part[1])
                change_widget.setStyleSheet('background-color: gray')
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
    from PySide2.QtWidgets import QApplication

    app = QApplication(sys.argv)
    # Open the main window
    from Song import Song
    from pathlib import Path

    song_diff: SongDiff = SongDiff(Song(Path("D:\\Git\\SongBeamer_SimilarSongFinder\\Songs\\95 Krasse Thesen.sng")),
                                   Song(Path("D:\\Git\\SongBeamer_SimilarSongFinder\\Songs\\99 Luftballons.sng")))
    song_diff.show()
    # Quit when the user exits the program
    sys.exit(app.exec_())
