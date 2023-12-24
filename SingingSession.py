from typing import List, Optional

from MarkupObject import MarkupObject


class SingingSession:
    def __init__(self, markup: List[MarkupObject]):
        self._markup = markup

        self._current_word_number = 0
        self._current_line = ''
        self._words_in_line: List[str] = []

    def get_current_line_sung(self, time_in_ms: int) -> Optional[str]:
        if self._current_word_number >= len(self._markup):
            return None

        if self._markup[self._current_word_number].offset > time_in_ms:
            return None

        word = self._markup[self._current_word_number].word

        if word == 'show_next_lines' or word == 'show_blank_line':
            self._words_in_line.clear()
            self._current_line = ''
            self._current_word_number += 1
            return word

        self._words_in_line.append(word)
        self._current_word_number += 1
        self._current_line = ' '.join(self._words_in_line)
        return self._current_line
