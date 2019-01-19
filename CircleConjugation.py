import sys
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from math import sqrt
from sympy import Line2D
from sympy import sympify, Rational
from sympy.geometry import Point2D, Segment2D, Circle
import matplotlib.lines as mlines
import matplotlib.path
import math
import random


class Window(QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        # buttons
        self.button_plot = QPushButton('Plot')
        self.button_random = QPushButton('Random')
        self.button_plot.clicked.connect(self.__plot)
        self.button_random.clicked.connect(self.__random)

        self.main_circle = QLineEdit()
        self.main_circle.setText("главный круг: x, y, r")
        self.circle = QLineEdit()
        self.circle.setText("круг сопряжения: r")
        self.line = QLineEdit()
        self.line.setText("точки прямой: x1, y1, x2, y2")

        layout_global = QHBoxLayout()
        layout_left = QVBoxLayout()
        layout_left.addWidget(self.toolbar)
        layout_left.addWidget(self.canvas)
        layout_right = QVBoxLayout()
        layout_right.addWidget(self.main_circle)
        layout_right.addWidget(self.circle)
        layout_right.addWidget(self.line)
        layout_right.addWidget(self.button_plot)
        layout_right.addWidget(self.button_random)
        layout_global.addLayout(layout_left)
        layout_global.addLayout(layout_right)

        self.setLayout(layout_global)
        self.resize(900, 700)

    def __prepare_variable(self):

        # __initialization__
        self.extreme_points_of_main_line = []               # крайние точки главной прямой
        self.r_small_circle = 0
        self.big_circle = []
        self.main_line_points = []                          # x1, y1, x2, y2
        self.point_intersect_big_and_small_circle = []      # пересечение маленьких окружностей с основной
        self.center_of_small_circles = []                   # центры маленьких окружностей
        self.point_intersect_on_line = []                   # точки пересечения маленьких окружностей с линией
        self.style = 1
        # __end of initialization__

        temp = self.main_circle.text().split()
        self.big_circle = []
        self.big_circle.append(int(temp[0]))
        self.big_circle.append(int(temp[1]))
        self.big_circle.append(int(temp[2]))
        temp = self.circle.text().split()
        self.r_small_circle = int(temp[0])
        temp = self.line.text().split()
        self.main_line_points.append(int(temp[0]))
        self.main_line_points.append(int(temp[1]))
        self.main_line_points.append(int(temp[2]))
        self.main_line_points.append(int(temp[3]))

    def __plot(self):
        self.__prepare_variable()

        p1 = [self.main_line_points[0], self.main_line_points[1]]
        p2 = [self.main_line_points[2], self.main_line_points[3]]

        self.figure.clear()
        circle = plt.Circle(((self.big_circle[0]), (self.big_circle[1])),
                            radius=(self.big_circle[2]),
                            fill=False,
                            color='b')
        circle_for_help = plt.Circle(((self.big_circle[0]), (self.big_circle[1])),
                             radius=(self.big_circle[2]) + self.r_small_circle,
                             fill=False,
                             linestyle='--',
                             color='w')
        self.figure.gca().add_patch(circle)
        self.figure.gca().add_patch(circle_for_help) #Без этого не работает!
        self.figure.gca().axis('scaled')

        self.__auxiliary_lines()
        self.find_intersect_circle_and_circle()

        self.style = 0
        temp = self.__plot_line(p1, p2)     # рисовка основной красной линии возвращает её крайние точки
        self.extreme_points_of_main_line.append(temp[0])
        self.extreme_points_of_main_line.append(temp[1])
        print("Крайние точки красной линии (x1 y1) (x2,y2): ", self.extreme_points_of_main_line)

        distance = self.distance_from_point_to_line([self.big_circle[0], self.big_circle[1]], p1, p2)
        if distance < self.big_circle[2]:
            print("четыре сопрягающих окружности")
            self.intersection_with_line(4)
            self.draw_arc()
        elif distance <= (2 * self.r_small_circle + self.big_circle[2]):    # дистанция от прямой до центра окружности
                                                # меньше чем диаметр малой окружности + радиус большой окружности
            print("две сопрягающих окружности")
            self.intersection_with_line(2)
            self.draw_arc()
        else:
            print("невозможно постоить сопрягающую окружность")

        self.canvas.draw()

    def __plot_line(self, p1, p2, stop=0):
        xmin, xmax = self.figure.gca().get_xbound()
        if (p2[0] == p1[0]):
            xmin = xmax = p1[0]
            ymin, ymax = self.figure.gca().get_ybound()
        else:
            ymax = p1[1] + (p2[1] - p1[1]) / (p2[0] - p1[0]) * (xmax - p1[0])
            ymin = p1[1] + (p2[1] - p1[1]) / (p2[0] - p1[0]) * (xmin - p1[0])
        if self.style == 0:     # стиль основных и дополнительных линий
            line = mlines.Line2D([xmin, xmax], [ymin, ymax], color='r')
            self.style = 1      # стиль основных и дополнительных линий
        else:
            line = mlines.Line2D([xmin, xmax], [ymin, ymax], linestyle='--', color='b')

        first_extreme_point = [xmin, ymin]
        second_extreme_point = [xmax, ymax]
        if stop == 0:
            self.figure.gca().add_line(line)
            self.figure.gca().axis('scaled')
        # self.canvas.draw() #вероятно не нужно
        return first_extreme_point, second_extreme_point

    def intersection_with_circle(self, point1, point2):
        r = self.r_small_circle
        R = self.big_circle[2]
        try:
            # Point A, B and C
            A = Point2D(self.big_circle[0], self.big_circle[1])
            B = Point2D(point1[0], point1[1])
            C = Point2D(point2[0], point2[1])

            # Segment from B to C - line
            line = Segment2D(B, C)
            c = Circle(A, R+r)
            result_of_intersect = c.intersection(line)

            # print(result_of_intersect)
            temp1 = result_of_intersect[0]
            temp2 = result_of_intersect[1]
            temp1 = str(temp1)[7:]
            temp2 = str(temp2)[7:]
            # print(temp1)
            # print(temp2)
            # print(eval(temp1))
            # print(eval(temp2))
            p1 = eval(temp1)
            p2 = eval(temp2)
            # point1 = mlines.Line2D([p1[0], p2[0]], [p1[1], p2[1]], color='b')
            # self.figure.gca().add_line(point1)
            return p1, p2
        except:
            return -666

    def intersection_with_line(self, key):
        self.__for_debug("Поиск точек пересечения малых окружностей с прямой")
        rang = 0
        if key == 2:
            rang = 2
        elif key == 4:
            rang = 4
        print("ДЕБАГ: x1,y1 - крайняя точка главной прямой", self.extreme_points_of_main_line[0][0],
              self.extreme_points_of_main_line[0][1])
        print("ДЕБАГ: x2,y2 - крайняя точка главной прямой", self.extreme_points_of_main_line[1][0],
              self.extreme_points_of_main_line[1][1])
        print("ДЕБАГ: центры малых окружностей ", self.center_of_small_circles)
        for i in range(rang):
            try:
                result = self.find_intersect_circle_and_line(self.extreme_points_of_main_line[0][0],
                                                             self.extreme_points_of_main_line[0][1],
                                                             self.extreme_points_of_main_line[1][0],
                                                             self.extreme_points_of_main_line[1][1],
                                                             self.center_of_small_circles[i][0],
                                                             self.center_of_small_circles[i][1],
                                                             self.r_small_circle + 0.1)
                if result != []:
                    self.point_intersect_on_line.append(result)
            except:
                print("ERROR")
        print("Точки на прямой :", self.point_intersect_on_line)

    def find_intersect_circle_and_line(self, x1, y1, x2, y2, x3, y3, r):
        A = Point2D(x1, y1)
        B = Point2D(x2, y2)
        C = Point2D(x3, y3)
        F = Line2D(A, B)
        c = Circle(C, sympify(Rational(r), rational=True))
        i_0 = F.intersection(c)
        temp1 = i_0[0]
        temp2 = i_0[1]
        temp1 = str(temp1)[7:]
        temp2 = str(temp2)[7:]
        temp1 = eval(temp1)
        temp2 = eval(temp2)
        x = (temp1[0] + temp2[0])/2
        y = (temp1[1] + temp2[1])/2
        return [x, y]

    def __auxiliary_lines(self):
        self.__for_debug("построение вспомогательных линий")
        for i in range(2):      # две линии (верхняя и нижняя)
            print("прямая № ", i)
            x1, y1, x2, y2 = self.main_line_points[0], self.main_line_points[1], self.main_line_points[2], self.main_line_points[3]
            normal_x = x2 - x1    # точки для построения вектора нормали
            normal_y = y2 - y1
            if i == 0:
                normal_points = [normal_y, -normal_x]   # правый\верхний вектор
            else:
                normal_points = [-normal_y, normal_x]   # левый\нижний вектор
            normal_points = [normal_points[0] + x1, normal_points[1] + y1]  # вектор первой точки заданного отрезка
            print("точка через которую строится вспомогательный вектор ", normal_points)
            # p1 = [x1, y1]
            # p2 = [normal_points[0], normal_points[1]]
            # self.__plot_line(p1,p2)   #рисовка вспомокательных линий для построения других вспомокательных линий :)

            # нахождение отрезка заданной длины
            r = self.r_small_circle
            distance = ((normal_points[0] - x1)**2 + (normal_points[1] - y1)**2)**(1/2)    # длина отрезка
            k = r/distance
            Xc = x1 + (normal_points[0] - x1) * k
            Yc = y1 + (normal_points[1] - y1) * k
            line_len_r = [Xc, Yc, x1, y1]
            normal_x = line_len_r[2] - line_len_r[0]
            normal_y = line_len_r[3] - line_len_r[1]
            normal_points = [normal_y, -normal_x]
            normal_points = [normal_points[0] + line_len_r[0], normal_points[1] + line_len_r[1]]
            p1 = [line_len_r[0], line_len_r[1]]      # точка h она же q
            p2 = [normal_points[0], normal_points[1]]

            print("точки вспомогательного отрезка ", p1, " ", p2)
            first_extreme_point, second_extreme_point = self.__plot_line(p1, p2, 1)
            intersection_points = self.intersection_with_circle(first_extreme_point, second_extreme_point)
            if intersection_points != -666:
                self.center_of_small_circles.append(intersection_points[0])
                self.center_of_small_circles.append(intersection_points[1])
            print("найденные центры малых окружностей прямой №", i, " : ", intersection_points)
            # new_line2 = mlines.Line2D([line_len_r[0], normal_points[0]], [line_len_r[1], normal_points[1]], color='g')
            # self.figure.gca().add_line(new_line2)
        self.__for_debug("конец построения вспомогательных линий")

    def draw_arc(self):
        self.__for_debug("РИСОВАНИЕ СЕКТОРОВ")
        for i in range(len(self.center_of_small_circles)):
            x0, y0 = self.center_of_small_circles[i][0], self.center_of_small_circles[i][1]
            x1, y1 = self.point_intersect_on_line[i][0], self.point_intersect_on_line[i][1]
            x2, y2 = self.point_intersect_big_and_small_circle[i][0], self.point_intersect_big_and_small_circle[i][1]
            width = 2 * self.r_small_circle
            height = 2 * self.r_small_circle

            angle_1 = math.degrees(math.atan2(y1 - y0, x1 - x0))
            angle_2 = math.degrees(math.atan2(y2 - y0, x2 - x0))
            print("START_ARC ", angle_1)
            print("END_ARC ", angle_2)
            Z = lambda x: 360 + x
            if angle_1 < 0:
                temp_1 = Z(angle_1)
            else:
                temp_1 = angle_1
            if angle_2 < 0:
                temp_2 = Z(angle_2)
            else:
                temp_2 = angle_2

            if temp_1 > temp_2:
                d1 = temp_1 - temp_2
                d2 = 360 + temp_2 - temp_1
                if d1 > d2:
                    start_angle = temp_1
                    end_angle = temp_2
                else:
                    start_angle = temp_2
                    end_angle = temp_1
            else:
                d1 = temp_2 - temp_1
                d2 = 360 + temp_1 - temp_2
                if d1 > d2:
                    start_angle = temp_2
                    end_angle = temp_1
                else:
                    start_angle = temp_1
                    end_angle = temp_2

            arc = matplotlib.patches.Arc((x0, y0),
                                         width,
                                         height,
                                         theta1=start_angle,
                                         theta2=end_angle)
            self.figure.gca().add_patch(arc)

    def find_intersect_circle_and_circle(self):
        self.__for_debug("Поиск точек пересечения круга и малых кругов")
        for i in self.center_of_small_circles:
            temp = self.point_on_line(self.big_circle[0], self.big_circle[1], i[0], i[1], self.big_circle[2])
            self.point_intersect_big_and_small_circle.append([temp[0], temp[1]])
        print(self.point_intersect_big_and_small_circle)
        # new_line2 = mlines.Line2D([i[0], self.point_intersect_big_and_small_circle[0][0]], [i[1], self.point_intersect_big_and_small_circle[0][1]], color='y')
        # self.figure.gca().add_line(new_line2)

    @staticmethod
    def point_on_line(xa, ya, xb, yb, dist):
        """координаты точки на прямой на указанном расстоянии от начала этой прямой"""
        rab = sqrt((xb - xa)**2 + (yb - ya)**2)
        k = dist / rab
        xc = xa + (xb - xa) * k
        yc = ya + (yb - ya) * k
        return xc, yc

    @staticmethod
    def distance_from_point_to_line(p1, p2, p3):
        """расстояние от точки р1 до прямой р2---р3"""
        x0 = p1[0]
        y0 = p1[1]
        x1 = p2[0]
        y1 = p2[1]
        x2 = p3[0]
        y2 = p3[1]
        up = math.fabs(((y2-y1)*x0)-((x2-x1)*y0)+(x2*y1)-(y2*x1))
        down = (((y2-y1)**2) + ((x2-x1)**2))**(1/2)
        result = up/down
        print("Дистанция от круга до прямой: ", result)
        return result

    @staticmethod
    def __for_debug(name_func="##"):
        print()
        print("#####################################################################")
        print("########################  ", name_func, "  ##############################")

    def __random(self):
        x1 = random.randint(-20, 20)
        y1 = random.randint(-20, 20)
        r1 = random.randint(1, 10)
        s = str(x1) + " " + str(y1) + " " + str(r1)
        self.main_circle.setText(s)
        x2 = random.randint(x1 - 5, x1 + 5)
        y2 = random.randint(y1 - 5, y1 + 5)
        x3 = random.randint(x1 - 5, x1 + 5)
        y3 = random.randint(y1 - 5, y1 + 5)
        s = str(x2) + " " + str(y2) + " " + str(x3) + " " + str(y3)
        self.line.setText(s)
        r2 = random.randint(1, 6)
        self.circle.setText(str(r2))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec_())
