import sys
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import random
import shapely.geometry as sg
import descartes


class Window(QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        # buttons
        self.button_key = 3  # 1 - синий полигон, 2 - красный полигон, 3 - оба полигона
        self.button_first_figure = QPushButton('Синий полигон')
        self.button_first_figure.clicked.connect(self.__select_blue_figure)
        self.button_second_figure = QPushButton('Красный полигон')
        self.button_second_figure.clicked.connect(self.__select_red_figure)
        self.button_all_figure = QPushButton('Оба полигона')
        self.button_all_figure.clicked.connect(self.__select_all_figure)
        self.button_random = QPushButton('Random')
        self.button_random.clicked.connect(self.__random)
        self.button_shift_left = QPushButton('<-')
        self.button_shift_left.clicked.connect(self.__left)
        self.button_shift_up = QPushButton('/\\')
        self.button_shift_up.clicked.connect(self.__up)
        self.button_shift_down = QPushButton('\/')
        self.button_shift_down.clicked.connect(self.__down)
        self.button_shift_right = QPushButton('->')
        self.button_shift_right.clicked.connect(self.__right)
        self.line = QLineEdit()
        self.line.setText("5 4")

        layout_global = QHBoxLayout()
        layout_left = QVBoxLayout()
        layout_left.addWidget(self.toolbar)
        layout_left.addWidget(self.canvas)
        layout_right = QVBoxLayout()
        layout_right.addWidget(self.button_first_figure)
        layout_right.addWidget(self.button_second_figure)
        layout_right.addWidget(self.button_all_figure)
        layout_right.addWidget(self.button_random)
        layout_right.addWidget(self.line)
        layout_right.addWidget(self.button_shift_left)
        layout_right.addWidget(self.button_shift_up)
        layout_right.addWidget(self.button_shift_down)
        layout_right.addWidget(self.button_shift_right)
        layout_global.addLayout(layout_left)
        layout_global.addLayout(layout_right)

        self.blue_figure = []
        self.red_figure = []
        self.intersect_figure = []

        self.setLayout(layout_global)
        self.resize(900, 700)

    def __select_blue_figure(self):
        self.button_key = 1
        return 0

    def __select_red_figure(self):
        self.button_key = 2
        return 0

    def __select_all_figure(self):
        self.button_key = 3
        return 0

    def __up(self):
        return 0

    def __down(self):
        return 0

    def __right(self):
        return 0

    def __left(self):
        return 0

    def __random(self):
        __number_of_points = self.line.text().split()
        points = []
        for i in range(int(__number_of_points[0])):
            x = int(random.randint(0, 20))
            y = int(random.randint(0, 20))
            points.append((x, y))
        points.append(points[0])

        if self.button_key == 1:
            self.blue_figure = points
            self.__plot()

        elif self.button_key == 2:
            self.red_figure = points
            self.__plot()

        elif self.button_key == 3:
            self.button_key = 2
            self.blue_figure = points
            self.__random()
        return 0

    def __plot(self):
        self.figure.clear()
        __intersected_figure = self.__find_intersect()
        if __intersected_figure == 0:
            __intersected_figure = [(0, 0), (1, 1)]
        __blue_figure = plt.Polygon(self.blue_figure, color="b", closed=False)
        __red_figure = plt.Polygon(self.red_figure, color="r", closed=False)

        self.figure.gca().add_patch(__blue_figure)
        self.figure.gca().add_patch(__red_figure)
        self.figure.gca().add_patch(descartes.PolygonPatch(__intersected_figure, fc='g', alpha=0.5))
        self.figure.gca().axis('scaled')
        self.canvas.draw()

    def __find_intersect(self):
        p1 = sg.Polygon(self.blue_figure).buffer(.01)
        p2 = sg.Polygon(self.red_figure).buffer(.01)
        p3 = p1.intersection(p2)
        print(self.red_figure)
        print(self.blue_figure)
        print(p3)
        temp = str(p3)[0:2]
        if temp[0] == "P":
            print("POLY")
            temp = str(p3)[10::]
            temp = temp[:-2:]
            temp = temp.split(",")
            print(temp)
            res = []
            for i in temp:
                i.split()
                res.append((i[0], i[1]))
            print(res)
        elif temp[0] == "M":
            print("MULTY")
            temp = str(p3)[13::]
            print(temp)
        elif temp[0] == "G":
            return 0

        return p3


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec_())
