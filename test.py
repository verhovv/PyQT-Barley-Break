import sys

from settings import *


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        QMessageBox.about(self, "ПОБЕДА", f"Вы побидели за X ходов")

        self.show()


if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())
