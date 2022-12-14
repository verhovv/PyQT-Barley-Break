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

        # labels setting
        self.timeLabel = QLabel('Время: 0', self)
        self.timeLabel.resize(150, 25)
        self.timeLabel.setFont(MAIN_FONT)
        self.timeLabel.move(10, 20)

        self.recordLabel = QLabel(f'Рекорд: {record(plates_width * plates_height)}', self)
        self.recordLabel.resize(150, 25)
        self.recordLabel.setFont(MAIN_FONT)
        self.recordLabel.move(self.timeLabel.x(), self.timeLabel.y() + 15)

        self.advice = QLabel('Нажмите "Alt", чтобы увидеть правильное расположение', self)
        self.advice.setFont(MAIN_FONT)
        self.advice.resize(MAIN_FONT.pointSize() * len(self.advice.text()),
                           MAIN_FONT.pointSize() + 5)
        self.advice.move(self.width() // 2 - self.advice.width() // 2,
                         3
                         )

        # main window setting
        self.setWindowTitle("PyQT Barley-Break")
        self.setMaximumSize(QSize(*WINDOW_SIZE))
        self.setMinimumSize(QSize(*WINDOW_SIZE))
        self.setWindowIcon(QIcon(QPixmap(QImage('assets/images/icon.png'))))

        # initializing imageButton (to put small version of image here)
        self.imageButton = QPushButton(self)

        # initializing the settingWindow from settings.py
        self.settingWindow = SettingWindow()

        # settingButton setting
        self.settingButton = QPushButton('Настройки', self)
        self.settingButton.clicked.connect(self.settingWindow.show)
        self.settingButton.move(WINDOW_WIDTH - self.settingButton.width() - 10, 10)

        # regenerateButton setting
        self.regenerateButton = QPushButton('Пересобрать', self)
        self.regenerateButton.resize(self.settingButton.size())
        self.regenerateButton.move(self.settingButton.x(),
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
                Plate(f'{y * plates_width + x + 1}', self, [x, y], pixmap)

        # deleting the last plate
        Plate.plates[-1].setParent(None)
        Plate.plates = Plate.plates[:-1]

        # mixing the plates
        Plate.generate_plates()

        # setting enable to all the plates
        Plate.set_enabled(True)

        # setting labels text
        self.timeLabel.setText(f'Время: 0 секунд')
        self.recordLabel.setText(f'Рекорд: {record(plates_width * plates_height)}')
        self.recordLabel.resize(MAIN_FONT.pointSize() * len(self.timeLabel.text()),
                                MAIN_FONT.pointSize() + 5)

        empty_plate_coords[0] = plates_width - 1
        empty_plate_coords[1] = plates_height - 1


if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())
