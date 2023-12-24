from typing import List, Optional

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtWidgets import *

from LyricsWidget import LyricsWidget
from MarkingSession import MarkingSession
from MarkupObject import MarkupObject


class MarkingWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        geometry = self.parent().size()
        self.setGeometry(
            int(geometry.width() / 4),
            int(geometry.height() / 2),
            int(geometry.width() / 2),
            int(geometry.height() / 2))
        self._marking_session: Optional[MarkingSession] = None
        self._current_audio_name: Optional[str] = None
        self._init_ui()

    def end_marking_session(self):
        if self._marking_session is None:
            return

        self._player.stop()
        self._marking_session.close(f"Music/{self._current_audio_name}/markup")
        self._marking_session = None

    def continue_marking_session(self):
        with open(f'Music/{self._current_audio_name}/lyrics.txt', 'r', encoding='utf-8') as f:
            lyrics = f.readlines()
        lyrics = [line.replace('\n', '') for line in lyrics]

        with open(f'Music/{self._current_audio_name}/markup', 'r+', encoding='utf-8') as f:
            markup_strings = f.readlines()
            markup: List[List[MarkupObject]] = [[]]
            last_markup_object: Optional[MarkupObject] = None
            for mark in markup_strings:
                if mark == '':
                    return
                last_markup_object = MarkupObject.from_string(mark)
                markup[len(markup) - 1].append(last_markup_object)
                if last_markup_object.word == 'show_blank_line' or last_markup_object.word == 'show_next_lines':
                    markup.append([])

        self._lyrics_widget.init_lyrics(lyrics)
        self._marking_session = MarkingSession(lyrics, markup)

        [self._lyrics_widget.set_sung_line(line_to_push) for line_to_push in self._marking_session.get_marked_lines()]

        self._player.mediaStatusChanged.connect(
            lambda: self._player.setPosition(last_markup_object.offset if last_markup_object is not None else 0))
        self._player.play()

    def run_marking_session(self):
        with open(f'Music/{self._current_audio_name}/lyrics.txt', 'r', encoding='utf-8') as f:
            lyrics = f.readlines()
        lyrics = [line.replace('\n', '') for line in lyrics]

        self._lyrics_widget.init_lyrics(lyrics)
        self._marking_session = MarkingSession(lyrics, [[]])
        self._player.play()

    def set_volume(self, value: int):
        print(value)
        self._player.mediaStatusChanged.connect(lambda: self._player.audioOutput().setVolume(value / 100))

    def get_volume(self):
        return self._player.audioOutput().volume()

    def set_audio_name(self, name: str):
        self._current_audio_name = name

        url = QUrl(f"Music/{name}/song.mp3")
        self._player.setSource(url)

    def keyPressEvent(self, event: QKeyEvent):
        super().keyPressEvent(event)

        if self._marking_session is None:
            return

        if event.key() == Qt.Key.Key_Space:
            line_marked = self._marking_session.mark(self._player.position())
            if line_marked is None:
                self.end_marking_session()
                return
            self._lyrics_widget.set_sung_line(line_marked)

    def _init_ui(self):
        self._lyrics_widget = LyricsWidget(self)
        self._init_player()

    def _init_player(self):
        self._player = QMediaPlayer()
        self._audio_output = QAudioOutput()
        self._audio_output.setVolume(50)
        self._player.setAudioOutput(self._audio_output)
