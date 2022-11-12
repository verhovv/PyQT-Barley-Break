import sys

from settings import *
from plate import Plate


class SettingWindow(SettingsWindow):
    def onPress(self):
        super(SettingWindow, self).onPress()
        Window.make_plates(window)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.time = QLabel('Время: 0', self)
        self.time.resize(150, 25)
        self.time.setFont(MAIN_FONT)
        self.time.move(10, 20)

        self.setWindowTitle("PyQT Barley-Break")

        self.setMaximumSize(QSize(*WINDOW_SIZE))
        self.setMinimumSize(QSize(*WINDOW_SIZE))

        self.setWindowIcon(QIcon(QPixmap(QImage('icon.png'))))

        self.imageButton = QPushButton(self)

        self.settingsButton = QPushButton('Настройки', self)
        self.settingsButton.clicked.connect(self.show_setting_window)
        self.settingsButton.move(WINDOW_WIDTH - self.settingsButton.width() - 10, 10)

        self.settingWindow = SettingWindow()

        self.main_image = self.settingWindow.chooseImage()

        self.make_plates()

        self.show()

    def show_setting_window(self):
        self.settingWindow.show()

    def make_plates(self):
        from settings import SIZE_OF_PLATE, plates_width, plates_height, main_image

        self.mainImage = main_image
        self.mainImage = self.mainImage.scaled(plates_width * SIZE_OF_PLATE, plates_height * SIZE_OF_PLATE)

        self.imageButton.resize(plates_width * SIZE_OF_PLATE // 2, plates_height * SIZE_OF_PLATE // 2)
        self.imageButton.move(self.width() // 2 - self.imageButton.width() // 2, 50)

        self.imageButton.setIcon(QIcon(QPixmap(self.mainImage)))
        self.imageButton.setIconSize(self.imageButton.size())

        Plate.clear_plates()

        for x in range(plates_width):
            for y in range(plates_height):
                pixmap = QPixmap(
                    self.mainImage.copy(QRect(x * SIZE_OF_PLATE, y * SIZE_OF_PLATE, SIZE_OF_PLATE, SIZE_OF_PLATE))
                )

                Plate(self, [x, y], pixmap)

        Plate.plates[-1].setParent(None)
        Plate.plates = Plate.plates[:-1]

        Plate.generate_plates()


if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())
