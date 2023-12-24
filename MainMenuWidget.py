import os

from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt


class MainMenuWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        self.volume_slider = QSlider(Qt.Orientation.Vertical, self)
        self.volume_slider.setGeometry(25, 10, 10, 100)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)

        self.buttons_layout: QLayout = QHBoxLayout()
        self._init_mark_track_button(self.buttons_layout)
        self._init_continue_mark_track_button(self.buttons_layout)
        self._init_play_track_button(self.buttons_layout)

        self.central_layout: QVBoxLayout = QVBoxLayout(self)
        self.central_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.central_layout.addStretch()

        self.central_layout.addLayout(self.buttons_layout)
        self._init_track_list(self.central_layout)
        self._init_tracks()

        self.central_layout.addStretch()

        self.setLayout(self.central_layout)
        self._set_stylesheet()

    def _init_play_track_button(self, layout: QLayout):
        self.play_track_button: QPushButton = QPushButton()
        self.play_track_button.setText("Play")
        self.play_track_button.setEnabled(False)

        layout.addWidget(self.play_track_button)

    def _init_mark_track_button(self, layout: QLayout):
        self.mark_track_button: QPushButton = QPushButton()
        self.mark_track_button.setText("Mark")
        self.mark_track_button.setEnabled(False)

        layout.addWidget(self.mark_track_button)

    def _init_continue_mark_track_button(self, layout: QLayout):
        self.continue_mark_track_button: QPushButton = QPushButton()
        self.continue_mark_track_button.setText("Continue Marking")
        self.continue_mark_track_button.setEnabled(False)

        layout.addWidget(self.continue_mark_track_button)

    def _init_track_list(self, layout: QLayout):
        self.track_list = QListWidget(self)
        self.track_list.setMaximumSize(400, 500)

        self.track_list.setMinimumSize(300, 200)
        self.track_list.setBatchSize(10)

        self.track_list.clicked.connect(self._unlock_buttons)

        layout.addWidget(self.track_list)

    def _unlock_buttons(self):
        if os.path.exists(f'Music/{self.track_list.currentItem().text()}/markup'):
            self.continue_mark_track_button.setEnabled(True)
        self.mark_track_button.setEnabled(True)
        self.play_track_button.setEnabled(True)

    def _init_tracks(self):
        dir_names = os.listdir('Music')
        print(dir_names)
        for dir_name in dir_names:
            print(dir_name)
            self.track_list.addItem(dir_name)

    def _set_stylesheet(self):
        self.setStyleSheet(
            """
            QListWidget{
                background: transparent;
                background-color: rgba(255, 255, 255, 10%);     
                border-radius: 10px;
            }
            QListWidget::item{
                background: transparent;
                background-color: rgba(255, 255, 255, 25%);     
                border-color: rgba(255, 255, 255, 100%);     
                border-radius: 5px;
            }
            QListWidget::item::hover{
                background: transparent;
                background-color: rgba(255, 255, 255, 50%);     
            }
            QListWidget::item::selected{
                background: transparent;
                background-color: rgba(255, 255, 255, 60%);     
            }
            """
        )
