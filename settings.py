from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# window size constants
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = (600, 900)

# plates size
plates_width = 5
plates_height = 5
SIZE_OF_PLATE = int(WINDOW_WIDTH // max([plates_width, plates_height]) // 1.3)

# margins
PADDING = 2

# coordinates of empty plate
empty_plate_coords = [plates_width - 1, plates_height - 1]

# fonts
MAIN_FONT = QFont('Futurespore Cyrillic', 12)
LINK_FONT = QFont('Futurespore Cyrillic', 8)

# main image
mainImage = QImage('assets/images/pazzle.jpg')
image = QImage(mainImage)


class SettingsWindow(QMainWindow):
    SIZE = (400, 200)

    def __init__(self):
        # initializing font
        self.fontDB = QFontDatabase()
        self.fontDB.addApplicationFont("font.otf")

        super().__init__()

        # window settings
        self.setWindowTitle("Настройки")
        self.setMaximumSize(QSize(*SettingsWindow.SIZE))
        self.setMinimumSize(QSize(*SettingsWindow.SIZE))

        # spin boxes settings
        self.heightChoice = QSpinBox(self)
        self.heightChoice.move(self.width() // 3 * 2 - self.heightChoice.width() // 2,
                               self.height() // 5 * 3 - self.heightChoice.height() - 30)
        self.heightChoice.setMinimum(3)
        self.heightChoice.setMaximum(50)
        self.heightChoice.setValue(plates_height)

        self.widthChoice = QSpinBox(self)
        self.widthChoice.move(self.heightChoice.x(),
                              self.heightChoice.y() + self.heightChoice.height() + 10)
        self.widthChoice.setMinimum(3)
        self.widthChoice.setMaximum(50)
        self.widthChoice.setValue(plates_width)

        # labels settings
        self.heightLabel = QLabel("Количество плит по вертикали", self)
        self.heightLabel.resize(170, 25)
        self.heightLabel.move(self.heightChoice.x() - self.heightLabel.width() - 10,
                              self.heightChoice.y())

        self.widthLabel = QLabel("Количество плит по горизонтали", self)
        self.widthLabel.resize(170, 25)
        self.widthLabel.move(self.widthChoice.x() - self.widthLabel.width() - 10,
                             self.widthChoice.y())

        # line edit settings
        self.path = QLineEdit(self)
        self.path.setFont(LINK_FONT)
        self.path.move(self.heightChoice.x(),
                       self.heightChoice.y() - self.heightChoice.height() - 10)
        self.path.setEnabled(False)

        # button settings
        self.cimageButton = QPushButton("Выбрать изображение", self)
        self.cimageButton.resize(self.heightLabel.width(), self.cimageButton.height())
        self.cimageButton.move(self.heightLabel.x(),
                               self.heightLabel.y() - self.heightLabel.height() - 15)
        self.cimageButton.clicked.connect(self.chooseImage)

        self.applyButton = QPushButton('Применить', self)
        self.applyButton.move(self.width() // 2 - self.applyButton.width() // 2,
                              self.widthChoice.y() + self.widthChoice.height() + 20)
        self.applyButton.clicked.connect(self.onPress)

    # choosing image with file diolog
    def chooseImage(self):
        global mainImage

        # choosing full path of image with file diolog
        path = QFileDialog.getOpenFileName(self, 'Выбрать изображение', '',
                                           'Изображения (*.png *.xpm *.jpg *.jpeg)')
        if not path[0] and self.path.text():
            return

        # setting label
        self.path.setText(path[0].split('/')[-1])

        while not self.path.text():
            path = QFileDialog.getOpenFileName(self, 'Выбрать изображение', '',
                                               'Изображения (*.png *.xpm *.jpg *.jpeg)')
            self.path.setText(path[0].split('/')[-1])

        # setting mainImage
        mainImage = QImage(path[0])
        return mainImage

    # on setting button press
    def onPress(self):
        global plates_width, plates_height, SIZE_OF_PLATE, empty_plate_coords
        plates_width = self.widthChoice.value()
        plates_height = self.heightChoice.value()

        SIZE_OF_PLATE = int(WINDOW_WIDTH // max([plates_width, plates_height]) // 1.3)

        self.hide()
