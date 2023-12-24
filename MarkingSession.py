import time
from typing import List, Optional

from MarkupObject import MarkupObject


class MarkingSession:
    def __init__(self, lyrics: List[str], markup: List[List[MarkupObject]]):
        self._lines = [line.split(' ') for line in lyrics]
        for line in self._lines:
            if len(line) == 1 and line[0] == '':
                line.clear()

        for i in range(1, len(self._lines)):
            if len(self._lines[i]) == 0:
                self._lines[i - 1].append('show_blank_line')
            else:
                self._lines[i - 1].append('show_next_lines')
        self._lines[len(self._lines) - 1].append('show_blank_line')

        self._marked_lines: List[List[MarkupObject]] = markup

        self._marking_line = len(self._marked_lines) - 1
        self._marking_word = len(self._marked_lines[self._marking_line])

    def mark(self, time_in_ms: int) -> Optional[str]:
        if len(self._lines) == self._marking_line:
            return None

        (self._marked_lines[self._marking_line]
         .append(MarkupObject(self._lines[self._marking_line][self._marking_word], time_in_ms)))

        current_word = self._lines[self._marking_line][self._marking_word]
        if current_word == 'show_next_lines' or current_word == 'show_blank_line':
            self._marking_line += 1
            self._marking_word = 0
            self._marked_lines.append([])
            return current_word

        self._marking_word += 1
        return ' '.join([self._lines[self._marking_line][i] for i in range(self._marking_word)])

    def get_marked_lines(self):
        for line in self._marked_lines:
            for i in range(len(line)):
                if line[i].word == 'show_next_lines' or line[i].word == 'show_blank_line':
                    yield line[i].word
                else:
                    yield ' '.join(markup_object.word for markup_object in line[:(i + 1)])

    def close(self, file_to: str):
        with open(file_to, 'w', encoding='utf-8') as f:
            for line in self._marked_lines:
                for markup_object in line:
                    f.writelines(str(markup_object))
                    f.writelines('\n')



