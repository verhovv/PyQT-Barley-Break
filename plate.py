import random

from settings import *


class Plate(QPushButton):
    # list of all plates
    plates: list['Plate'] = list()

    def __init__(self, surface: QWidget, coords: list[int, int], pixmap: QPixmap):
        from settings import SIZE_OF_PLATE

        super().__init__(surface)

        self.surface = surface

        self.pixmap = pixmap

        self.coords = coords
        self.first_coords = self.coords.copy()

        self.resize(SIZE_OF_PLATE + PADDING, SIZE_OF_PLATE + PADDING)
        self.move_to_home()

        self.distance = (self.coords[0] - empty_plate_coords[0], self.coords[1] - empty_plate_coords[1])

        self.setIcon(QIcon(self.pixmap))
        self.setIconSize(self.pixmap.rect().size())

        self.clicked.connect(self.onClick)

        self.winMessageBox = QMessageBox()
        self.winMessageBox.setText('Вы выиграли!!!')

        Plate.plates.append(self)

    # moving plate to its coordinates
    def move_to_home(self):
        from settings import plates_width, plates_height

        self.move(self.surface.width() // 2 + self.coords[0] * self.width() - self.width() * plates_width // 2,
                  self.surface.height() // 5 * 4 + self.coords[
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

        # checking the 1-1 distance cases
        if abs(self.distance[0]) == abs(self.distance[1]):
            return False

        return True

    def onClick(self) -> None:
        from settings import empty_plate_coords

        self.distance = (self.coords[0] - empty_plate_coords[0], self.coords[1] - empty_plate_coords[1])

        if not self.can_move():
            return

        for i in range(2):
            self.coords[i] -= self.distance[i]
            empty_plate_coords[i] += self.distance[i]

        if self.check_is_won():
            self.winMessageBox.exec()

        self.move_on(self.x() - self.width() * self.distance[0], self.y() - self.height() * self.distance[1])

    # checking if won
    @staticmethod
    def check_is_won() -> bool:
        if sorted(Plate.plates, key=lambda x: x.coords) == Plate.plates:
            return True
        return False

    @staticmethod
    def clear_plates() -> None:
        for plate in Plate.plates:
            plate.setParent(None)
        Plate.plates.clear()

    @staticmethod
    def generate_plates() -> None:
        from settings import plates_width, plates_height

        coords = list()
        for x in range(plates_width):
            for y in range(plates_height):
                if x == plates_width - 1 and y == plates_height - 1:
                    continue
                coords.append([x, y])

        random.shuffle(coords)

        for i in range(len(Plate.plates)):
            Plate.plates[i].coords = coords[i]
            Plate.plates[i].move_to_home()
            Plate.plates[i].show()

        empty_plate_coords[0] = plates_width - 1
        empty_plate_coords[1] = plates_height - 1
