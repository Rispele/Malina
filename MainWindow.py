import os
import queue
from typing import Optional

from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QKeyEvent, QPaintEvent, QImage, QPalette, QBrush
from PyQt6.QtWidgets import QMainWindow

from MainMenuWidget import MainMenuWidget
from MarkingWidget import MarkingWidget
from PlayWidget import PlayWidget


class MainWindow(QMainWindow):
    button_stylesheet = "border: 1px solid black; border-radius: 20px;"

    def __init__(self):
        super().__init__()
        self._init_ui()

        self._bind_main_menu_widget_buttons()
        self._setup_background_changer()

    def _bind_main_menu_widget_buttons(self):
        self._main_menu_widget.play_track_button.clicked.connect(self._play_button_clicked)
        self._main_menu_widget.mark_track_button.clicked.connect(self._mark_button_clicked)
        self._main_menu_widget.continue_mark_track_button.clicked.connect(self._continue_mark_button_clicked)

    def _setup_background_changer(self):
        self._background_change_timer = QTimer()
        self._background_change_timer.setInterval(10000)
        self._background_change_timer.timeout.connect(self._change_background)
        self._background_change_timer.start()

        self._background_images = queue.Queue()
        [self._background_images.put(QImage(f'Backgrounds/{name}')) for name in os.listdir('Backgrounds')]
        self._change_background()

    def _change_background(self):
        image = self._background_images.get()
        self._background_images.put(image)

        self._background_image = image.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            transformMode=Qt.TransformationMode.SmoothTransformation
        )
        self._paint_background()

    def _paint_background(self):
        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(self._background_image))
        self.setPalette(palette)

    def paintEvent(self, a0: Optional[QPaintEvent]) -> None:
        self._paint_background()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Escape:
            volume = 50
            if self.centralWidget() == self._marking_widget:
                self._marking_widget.end_marking_session()
                volume = self._marking_widget.get_volume() * 100
            elif self.centralWidget() == self._play_widget:
                self._play_widget.end_singing_session()
                volume = self._play_widget.get_volume() * 100

            if self.centralWidget() != self._main_menu_widget:
                self._main_menu_widget = MainMenuWidget()
                self._main_menu_widget.volume_slider.setValue(volume)
                self._bind_main_menu_widget_buttons()
                self.setCentralWidget(self._main_menu_widget)

        if self.centralWidget() == self._marking_widget:
            self._marking_widget.keyPressEvent(event)

    def _play_button_clicked(self):
        track_chosen = self._get_track_chosen()
        self._play_widget = PlayWidget(self)
        self._play_widget.set_audio_name(track_chosen)
        self._play_widget.run_singing_session()
        self._play_widget.set_volume(self._main_menu_widget.volume_slider.value())

        self.setCentralWidget(self._play_widget)

    def _mark_button_clicked(self):
        track_chosen = self._get_track_chosen()
        self._marking_widget = MarkingWidget(self)
        self._marking_widget.set_audio_name(track_chosen)
        self._marking_widget.run_marking_session()
        self._marking_widget.set_volume(self._main_menu_widget.volume_slider.value())

        self.setCentralWidget(self._marking_widget)

    def _continue_mark_button_clicked(self):
        track_chosen = self._get_track_chosen()
        self._marking_widget = MarkingWidget(self)
        self._marking_widget.set_audio_name(track_chosen)
        self._marking_widget.continue_marking_session()
        self._marking_widget.set_volume(self._main_menu_widget.volume_slider.value())

        self.setCentralWidget(self._marking_widget)

    def _get_track_chosen(self) -> Optional[str]:
        item_chosen = self._main_menu_widget.track_list.currentItem()
        return item_chosen.text()

    def _init_ui(self):
        self._marking_widget: Optional[MarkingWidget] = None
        self._play_widget: Optional[PlayWidget] = None

        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.showFullScreen()

        self.setWindowTitle("Malina")
        self._main_menu_widget: MainMenuWidget = MainMenuWidget()
        self.setCentralWidget(self._main_menu_widget)
        self.setStyleSheet(
            """
            QPushButton{
                background: transparent;
                background-color: rgba(255, 255, 255, 50%);
                border-width: 1px white;
                border-radius: 5px;
                border-color: beige;
                font: bold 14px;
                padding: 6px;
            }
            QPushButton::hover{
                background-color: rgba(255, 255, 255, 75%);
            }
            QPushButton::pressed{
                background-color: rgba(255, 255, 255, 100%);
            }
            """
        )
