import sqlite3

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = (600, 900)

plates_width = 5
plates_height = 5

SIZE_OF_PLATE = int(WINDOW_WIDTH // max([plates_width, plates_height]) // 1.3)

PADDING = 2

empty_plate_coords = [plates_width - 1, plates_height - 1]

MAIN_FONT = QFont('Futurespore Cyrillic', 12)

main_image = None

database = sqlite3.connect('data.db')
cur = database.cursor()

def record(size=plates_width * plates_height):
    r = cur.execute(f"""
            SELECT record FROM records
            WHERE size={size}
            """).fetchone()

    return 0 if r is None else float(r[0])


class SettingsWindow(QMainWindow):
    SIZE = (400, 200)

    def __init__(self):
        self.fontDB = QFontDatabase()
        self.fontDB.addApplicationFont("font.otf")

        super().__init__()

        self.setWindowTitle("Настройки")

        self.setMaximumSize(QSize(*SettingsWindow.SIZE))
        self.setMinimumSize(QSize(*SettingsWindow.SIZE))

        self.heightChoice = QSpinBox(self)
        self.heightChoice.move(self.width() // 3 * 2 - self.heightChoice.width() // 2,
                               self.height() // 5 * 3 - self.heightChoice.height() - 30)
        self.heightChoice.setMinimum(2)
        self.heightChoice.setMaximum(50)
        self.heightChoice.setValue(plates_height)

        self.widthChoice = QSpinBox(self)
        self.widthChoice.move(self.heightChoice.x(),
                              self.heightChoice.y() + self.heightChoice.height() + 10)
        self.widthChoice.setMinimum(2)
        self.widthChoice.setMaximum(50)
        self.widthChoice.setValue(plates_width)

        self.heightLabel = QLabel("Количество плит по вертикали", self)
        self.heightLabel.resize(170, 25)
        self.heightLabel.move(self.heightChoice.x() - self.heightLabel.width() - 10,
                              self.heightChoice.y())

        self.widthLabel = QLabel("Количество плит по горизонтали", self)
        self.widthLabel.resize(170, 25)
        self.widthLabel.move(self.widthChoice.x() - self.widthLabel.width() - 10,
                             self.widthChoice.y())

        self.path = QLineEdit(self)
        self.path.setFont(MAIN_FONT)
        self.path.move(self.heightChoice.x(),
                       self.heightChoice.y() - self.heightChoice.height() - 10)
        self.path.setEnabled(False)

        self.cimageButton = QPushButton("Выбрать изображение", self)
        self.cimageButton.resize(self.heightLabel.width(), self.cimageButton.height())
        self.cimageButton.move(self.heightLabel.x(),
                               self.heightLabel.y() - self.heightLabel.height() - 15)
        self.cimageButton.clicked.connect(self.chooseImage)

        self.applyButton = QPushButton('Применить', self)
        self.applyButton.move(self.width() // 2 - self.applyButton.width() // 2,
                              self.widthChoice.y() + self.widthChoice.height() + 20)
        self.applyButton.clicked.connect(self.onPress)

    def chooseImage(self):
        global main_image

        path = QFileDialog.getOpenFileName(self, 'Выбрать изображение', '',
                                           'Изображения (*.png *.xpm *.jpg *.jpeg)')
        if not path[0] and self.path.text():
            return

        self.path.setText(path[0].split('/')[-1])

        while not self.path.text():
            path = QFileDialog.getOpenFileName(self, 'Выбрать изображение', '',
                                               'Изображения (*.png *.xpm *.jpg *.jpeg)')
            self.path.setText(path[0].split('/')[-1])

        main_image = QImage(path[0])
        return main_image

    def onPress(self):
        global plates_width, plates_height, SIZE_OF_PLATE, empty_plate_coords
        plates_width = self.widthChoice.value()
        plates_height = self.heightChoice.value()

        SIZE_OF_PLATE = int(WINDOW_WIDTH // max([plates_width, plates_height]) // 1.3)
        empty_plate_coords = [plates_width - 1, plates_height - 1]

        self.hide()
