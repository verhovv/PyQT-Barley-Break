import sys

from database import *
from plate import Plate
from settings import *


class SettingWindow(SettingsWindow):
    def onPress(self) -> None:
        super(SettingWindow, self).onPress()
        Window.make_plates(window)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # timeLabel setting
        self.timeLabel = QLabel('Время: 0', self)
        self.timeLabel.resize(150, 25)
        self.timeLabel.setFont(MAIN_FONT)
        self.timeLabel.move(10, 20)

        # recordLabel setting
        self.recordLabel = QLabel(f'Рекорд: {record(plates_width * plates_height)}', self)
        self.recordLabel.resize(150, 25)
        self.recordLabel.setFont(MAIN_FONT)
        self.recordLabel.move(self.timeLabel.x(), self.timeLabel.y() + 15)

        # main window setting
        self.setWindowTitle("PyQT Barley-Break")
        self.setMaximumSize(QSize(*WINDOW_SIZE))
        self.setMinimumSize(QSize(*WINDOW_SIZE))
        self.setWindowIcon(QIcon(QPixmap(QImage('icon.png'))))

        # initializing imageButton (to put small version of image here)
        self.imageButton = QPushButton(self)

        # initializing the settingWindow from settings.py
        self.settingWindow = SettingWindow()

        # taking mainImage from the file dialog
        self.settingWindow.chooseImage()

        # settingButton setting
        self.settingButton = QPushButton('Настройки', self)
        self.settingButton.clicked.connect(self.settingWindow.show)
        self.settingButton.move(WINDOW_WIDTH - self.settingButton.width() - 10, 10)

        # regenerateButton setting
        self.regenerateButton = QPushButton('Пересобрать\n↺', self)
        self.regenerateButton.resize(75, 75)
        self.regenerateButton.move(self.settingButton.x() + 12,
                                   self.settingButton.y() + self.settingButton.height() + 10)
        self.regenerateButton.clicked.connect(self.make_plates)

        # generating new plates
        self.make_plates()

        # showing main window
        self.show()

    # Generating new plates
    def make_plates(self) -> None:
        from settings import SIZE_OF_PLATE, plates_width, plates_height, mainImage, empty_plate_coords

        # resizing image to resolution we need
        image = mainImage.scaled(plates_width * SIZE_OF_PLATE, plates_height * SIZE_OF_PLATE)

        # imageButton setting
        self.imageButton.resize(plates_width * SIZE_OF_PLATE // 2, plates_height * SIZE_OF_PLATE // 2)
        self.imageButton.move(self.width() // 2 - self.imageButton.width() // 2, 50)
        self.imageButton.setIcon(QIcon(QPixmap(image)))
        self.imageButton.setIconSize(self.imageButton.size())

        # clearing all plates
        Plate.clear()

        # coordinates
        for x in range(plates_width):
            for y in range(plates_height):
                # creating individual pixmap for all the plates
                pixmap = QPixmap(
                    image.copy(QRect(x * SIZE_OF_PLATE, y * SIZE_OF_PLATE, SIZE_OF_PLATE, SIZE_OF_PLATE))
                )

                # creating all plates (adding to Plate.plates)
                Plate(self, [x, y], pixmap)

        # deleting the last one of the plates
        Plate.plates[-1].setParent(None)
        Plate.plates = Plate.plates[:-1]

        # mixing the plates
        Plate.generate_plates()

        # setting enable to all the plates
        Plate.set_enabled(True)

        # setting labels text
        self.timeLabel.setText(f'Время: 0 секунд')
        self.recordLabel.setText(f'Рекорд: {record(plates_width * plates_height)}')

        empty_plate_coords[0] = plates_width - 1
        empty_plate_coords[1] = plates_height - 1


if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())
