from typing import List, Optional

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QLabel


class LyricsWidget(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self._max_lines = 4
        self._max_sung_lines = 4
        self._current_sung_line = 0
        self._blank_lines_count = 0
        self._is_new_paragraph = False

        geometry = self.parent().geometry()
        size = self.parent().size()
        self.setGeometry(geometry.x(), geometry.y(), size.width(), size.height() / 2)
        self._lyrics: Optional[List[str]] = None
        self._singing_line: Optional[int] = None
        self._init_ui()

    def _init_ui(self):
        self._init_lines()

    def _init_lines(self):
        self.lines: List[QLabel] = [line for line in self.make_lines(self._max_lines, "QLabel {color: white;}")]
        self.sung_lines: List[QLabel] = [line for line in self.make_lines(self._max_sung_lines, "QLabel {color: yellow;}")]

    def make_lines(self, count: int, style_sheet: str):
        font_size = int(self.size().height() / count)
        for i in range(count):
            line = QLabel(self)
            line.setFont(QFont("Calibri", 26))
            line.setStyleSheet(style_sheet)
            line.setGeometry(0, font_size * i, self.parent().size().width(), font_size)
            line.setText('')
            yield line
            
    def init_lyrics(self, lyrics: List[str]):
        self._singing_line = 0
        self._lyrics = lyrics
        self._set_lines(0)

    def set_sung_line(self, line: str):
        print(line)
        if line == 'show_blank_line':
            self._singing_line += 1
            self._current_sung_line = 0
            self._is_new_paragraph = True

            self._clear_sung_lines()
            self._clear_singing_lines()
        elif line == 'show_next_lines':
            self._singing_line += 1
            if self._is_new_paragraph:
                self._is_new_paragraph = False
                self._current_sung_line = 0
                self._set_lines(self._singing_line)
                return

            if self._singing_line != 0 and self._singing_line % self._max_sung_lines == 0:
                self._set_lines(self._singing_line)
                self._current_sung_line = 0
                self._clear_sung_lines()
            else:
                self._current_sung_line += 1
        else:
            self.sung_lines[self._current_sung_line].setText(line)

    def _clear_singing_lines(self):
        [line.setText('') for line in self.lines]

    def _clear_sung_lines(self):
        [sung_line.setText('') for sung_line in self.sung_lines]

    def _set_lines(self, offset: int):
        end = False
        for i in range(self._max_lines):
            inner_offset = offset + i

            if inner_offset < len(self._lyrics) and not end:
                line = self._lyrics[inner_offset]
                end = line == ''
            else:
                line = ''
            self.lines[i].setText(line)
