import random
import time

from database import *
from settings import *


class Plate(QPushButton):
    # need flags
    is_started = False
    is_won = False

    # list of all plates
    plates: list['Plate'] = list()

    def __init__(self, mainWindow: QWidget, coords: list[int, int], pixmap: QPixmap):
        from settings import SIZE_OF_PLATE

        super().__init__(mainWindow)

        # our main window
        self.mainWindow = mainWindow

        # plate coordinates
        self.coords = coords
        self.first_coords = self.coords.copy()

        # setting the image of plate
        self.pixmap = pixmap
        self.setIcon(QIcon(self.pixmap))
        self.setIconSize(self.pixmap.rect().size())

        # resizing plate
        self.resize(SIZE_OF_PLATE + PADDING, SIZE_OF_PLATE + PADDING)

        # moving plate to its coordinates
        self.move_to_home()

        # distance from empty plate E[-1:1]
        self.distance = (self.coords[0] - empty_plate_coords[0], self.coords[1] - empty_plate_coords[1])

        # adding event on click on our plate-button
        self.clicked.connect(self.onClick)

        # timer setting
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.time_counter = 0

        # adding plate to plates list
        Plate.plates.append(self)

    # moving plate to its coordinates
    def move_to_home(self):
        from settings import plates_width, plates_height

        self.move(self.mainWindow.width() // 2 + self.coords[0] * self.width() - self.width() * plates_width // 2,
                  self.mainWindow.height() // 5 * 4 + self.coords[
                      1] * self.height() - self.height() * plates_height // 5 * 4)

    # animated moving
    def move_on(self, x, y) -> None:
        # animation properties
        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(100)
        self.anim.setStartValue(self.geometry())
        self.anim.setEndValue(QRect(x, y, self.width(), self.height()))

        # starting the animation
        self.anim.start()

    # returns True if can move
    def can_move(self) -> bool:
        # checking that distance is less or equals than 1
        for i in range(2):
            if abs(self.distance[i]) > 1:
                return False

        # checking the [1 == 1; -1 == -1] distance cases
        if abs(self.distance[0]) == abs(self.distance[1]):
            return False

        return True

    # plate click event
    def onClick(self) -> None:
        from settings import empty_plate_coords

        # distance from empty plate E[-1:1]
        self.distance = (self.coords[0] - empty_plate_coords[0], self.coords[1] - empty_plate_coords[1])

        if not self.can_move():
            return

        # editing plate and empty plate coordinates
        for i in range(2):
            self.coords[i] -= self.distance[i]
            empty_plate_coords[i] += self.distance[i]

        # moving the plate
        self.move_on(self.x() - self.width() * self.distance[0], self.y() - self.height() * self.distance[1])

        # editing flags
        if self.check_is_won():
            Plate.is_won = True

        if not Plate.is_started:
            self.timer.start(100)
            Plate.is_started = True

    # timer event
    def showTime(self) -> None:
        from settings import plates_height, plates_width
        if Plate.is_won:
            Plate.set_enabled(False)

            if record(plates_height * plates_width) > self.time_counter / 10 or record(
                    plates_height * plates_width) == 0:
                cur.execute(f"""INSERT INTO records
                VALUES({plates_width * plates_height}, {float(self.time_counter / 10)})""")
                database.commit()

                self.mainWindow.record.setText(f"Рекорд: {self.time_counter / 10}")

                QMessageBox.about(self, 'Вы выиграли!!! НОВЫЙ РЕКОРД!!!',
                                  f'Победа! Время: {self.time_counter / 10} секунд!'
                                  f'\nНовый рекорд!')
            else:
                QMessageBox.about(self, 'Вы выиграли!!!', f'Победа! Время: {self.time_counter / 10} секунд!')
            self.time_counter = 0

        if not Plate.is_started or Plate.is_won:
            self.timer.stop()
            return

        self.time_counter += 1
        self.mainWindow.timeLabel.setText(f'Время: {self.time_counter / 10} секунд')

    # checking if won
    @staticmethod
    def check_is_won() -> bool:
        if tuple(map(lambda x: x.first_coords, Plate.plates)) == tuple(map(lambda x: x.coords, Plate.plates)):
            return True
        return False

    @staticmethod
    def set_enabled(enabled: bool) -> None:
        for plate in Plate.plates:
            plate.setEnabled(enabled)

    @staticmethod
    def clear() -> None:
        for plate in Plate.plates:
            plate.setParent(None)
        Plate.plates.clear()

    @staticmethod
    # generating new plates
    def generate_plates() -> None:
        from settings import plates_width, plates_height

        Plate.is_won = False
        Plate.is_started = False

        coords = list(([x, y] for x in range(plates_width) for y in range(plates_height)))[:-1]

        k = 0 if plates_height % 2 else 1
        while (not k % 2) if plates_height % 2 else k % 2:
            k = 0
            random.shuffle(coords)

            for i in range(len(coords)):
                for j in range(i + 1, len(coords)):
                    if coords[i] > coords[j]:
                        k += 1
            k += plates_height

        for i in range(len(Plate.plates)):
            Plate.plates[i].coords = coords[i]
            Plate.plates[i].move_to_home()
            Plate.plates[i].show()

        empty_plate_coords[0] = plates_width - 1
        empty_plate_coords[1] = plates_height - 1
