import sys
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import random
import shapely.geometry as sg
from shapely.ops import polygonize, unary_union
import descartes
import numpy as np


class Window(QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        # buttons
        self.figure_key = 3  # 1 - синий полигон, 2 - красный полигон, 3 - оба полигона
        self.last_action = 0 # 1 - up, 2 - down, 3 - left, 4 - right
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
        self.figure_key = 1
        return 0

    def __select_red_figure(self):
        self.figure_key = 2
        return 0

    def __select_all_figure(self):
        self.figure_key = 3
        return 0

    def __up(self):
        print('UP!')
        if self.figure_key == 1:
            print(self.blue_figure)
            temp = [x[1] for x in self.blue_figure]
            for i in range(len(self.blue_figure)):
                self.blue_figure[i] = (self.blue_figure[i][0], temp[i] + 1)
        if self.figure_key == 2:
            print(self.red_figure)
            temp = [x[1] for x in self.red_figure]
            for i in range(len(self.red_figure)):
                self.red_figure[i] = (self.red_figure[i][0], temp[i] + 1)
        self.last_action = 1
        self.__plot()
        return 0

    def __down(self):
        print('DOWN!')
        if self.figure_key == 1:
            print(self.blue_figure)
            temp = [x[1] for x in self.blue_figure]
            for i in range(len(self.blue_figure)):
                self.blue_figure[i] = (self.blue_figure[i][0], temp[i] - 1)
        if self.figure_key == 2:
            print(self.red_figure)
            temp = [x[1] for x in self.red_figure]
            for i in range(len(self.red_figure)):
                self.red_figure[i] = (self.red_figure[i][0], temp[i] - 1)
        self.last_action = 2
        self.__plot()
        return 0

    def __right(self):
        print('Right!')
        if self.figure_key == 1:
            print(self.blue_figure)
            temp = [x[0] for x in self.blue_figure]
            for i in range(len(self.blue_figure)):
                self.blue_figure[i] = (temp[i] + 1, self.blue_figure[i][1])
        if self.figure_key == 2:
            print(self.red_figure)
            temp = [x[0] for x in self.red_figure]
            for i in range(len(self.red_figure)):
                self.red_figure[i] = (temp[i] + 1, self.red_figure[i][1])
        self.last_action = 4
        self.__plot()
        return 0

    def __left(self):
        print('Left!')
        if self.figure_key == 1:
            print(self.blue_figure)
            temp = [x[0] for x in self.blue_figure]
            for i in range(len(self.blue_figure)):
                self.blue_figure[i] = (temp[i] - 1, self.blue_figure[i][1])
        if self.figure_key == 2:
            print(self.red_figure)
            temp = [x[0] for x in self.red_figure]
            for i in range(len(self.red_figure)):
                self.red_figure[i] = (temp[i] - 1, self.red_figure[i][1])
        self.last_action = 3
        self.__plot()
        return 0

    def __random(self):
        __number_of_points = self.line.text().split()
        points = []
        for i in range(int(__number_of_points[0])):
            x = int(random.randint(0, 20))
            y = int(random.randint(0, 20))
            points.append((x, y))
        points.append(points[0])

        if self.figure_key == 1:
            self.blue_figure = points
            self.__plot()

        elif self.figure_key == 2:
            self.red_figure = points
            self.__plot()

        elif self.figure_key == 3:
            self.figure_key = 2
            self.blue_figure = points
            self.__random()
        return 0

    def __plot(self):
        try:
            self.figure.clear()
            __blue_figure = plt.Polygon(self.blue_figure, color="b", closed=False)
            __red_figure = plt.Polygon(self.red_figure, color="r", closed=False)
            self.figure.gca().add_patch(__blue_figure)
            self.figure.gca().add_patch(__red_figure)
            try:
                __intersected_figure = self.__find_intersect()
                __yellow_figure = descartes.PolygonPatch(__intersected_figure, fc='y', alpha=1)
                self.figure.gca().add_patch(__yellow_figure)
            except:
                print("Without Intersect")
                # self.__random()
                # self.__plot()
            self.figure.gca().axis('scaled')
            self.canvas.draw()
        except:
            print("EXEPTION")

    def __find_intersect(self):
        p1 = self.blue_figure
        p2 = self.red_figure
        p1 = self.__simplify(p1)
        p2 = self.__simplify(p2)
        p3 = p1.intersection(p2)
        return p3

    def __simplify(self, points):
        x = []
        y = []
        for i in points:
            x.append(i[0])
            y.append(i[1])
        ls = sg.LineString(np.c_[x, y])
        lr = sg.LineString(ls.coords[:] + ls.coords[0:1])
        lr.is_simple  # False
        mls = unary_union(lr)
        mls.geom_type  # MultiLineString'
        mp = sg.MultiPolygon(list(polygonize(mls)))
        return mp


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec_())
