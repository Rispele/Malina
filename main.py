import sys

from PyQt6.QtWidgets import QApplication

from MainWindow import MainWindow

app = QApplication(sys.argv)

m = MainWindow()
m.show()

app.exec()