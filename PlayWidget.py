import os.path
from typing import Optional

from PyQt6.QtCore import QUrl, pyqtSignal, QTimer
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtWidgets import QWidget

from LyricsWidget import LyricsWidget
from MarkupObject import MarkupObject
from SingingSession import SingingSession


class PlayWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self._current_audio_name: Optional[str] = None
        self._singing_session: Optional[SingingSession] = None
        self._lyrics_poll_timer: Optional[QTimer] = None

        geometry = self.parent().size()
        self.setGeometry(
            int(geometry.width() / 4),
            int(geometry.height() / 2),
            int(geometry.width() / 2),
            int(geometry.height() / 2))
        self._init_ui()

    def end_singing_session(self):
        if self._singing_session is None:
            return

        self._lyrics_poll_timer.stop()
        self._player.stop()
        self._singing_session = None

    def run_singing_session(self):
        with open(f'Music/{self._current_audio_name}/lyrics.txt', 'r', encoding='utf-8') as f:
            lyrics = f.readlines()
        lyrics = [line.replace('\n', '') for line in lyrics]

        if os.path.exists(f'Music/{self._current_audio_name}/markup'):
            with open(f'Music/{self._current_audio_name}/markup', 'r', encoding='utf-8') as f:
                markup = f.readlines()
        else:
            markup = []
        markup = [MarkupObject.from_string(line.replace('\n', '')) for line in markup]

        self._lyrics_widget.init_lyrics(lyrics)
        self._singing_session = SingingSession(markup)
        self._setup_lyrics_poller()

        self._player.play()

    def set_volume(self, value: int):
        self._player.mediaStatusChanged.connect(lambda: self._player.audioOutput().setVolume(value / 100))

    def get_volume(self):
        return self._player.audioOutput().volume()

    def set_audio_name(self, name: str):
        self._current_audio_name = name

        url = QUrl(f"Music/{name}/song.mp3")
        self._player.setSource(url)

    def _setup_lyrics_poller(self):
        self._lyrics_poll_timer = QTimer()
        self._lyrics_poll_timer.setInterval(50)
        self._lyrics_poll_timer.timeout.connect(self._poll_lyrics)
        self._lyrics_poll_timer.start()

    def _poll_lyrics(self):
        new_line = self._singing_session.get_current_line_sung(self._player.position())
        if new_line is None:
            return
        self._lyrics_widget.set_sung_line(new_line)

    def _init_ui(self):
        self._lyrics_widget = LyricsWidget(self)
        self._init_player()

    def _init_player(self):
        self._player = QMediaPlayer()
        self._audio_output = QAudioOutput()
        self._audio_output.setVolume(50)
        self._player.setAudioOutput(self._audio_output)
