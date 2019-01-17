import sys
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from math import sqrt
from sympy import Circle, Line2D
from sympy import sympify, Symbol, Rational
from sympy.geometry import Point2D, Segment2D, Circle
import matplotlib.lines as mlines
import math
import pylab
import matplotlib.path

#0 -3 5 -5
class Window(QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        # buttons
        self.button_plot = QPushButton('Plot')
        self.button_plot.clicked.connect(self.__plot)

        self.main_circle = QLineEdit()
        # self.main_circle.setText("главный круг: x, y, r")
        self.main_circle.setText("4 5 7")
        self.circle = QLineEdit()
        # self.circle.setText("круг сопряжения: r")
        self.circle.setText("2 2 4")
        self.line = QLineEdit()
        self.line.setText("точки прямой: x1, y1, x2, y2")
        self.line.setText("0 15 10 20")

        layout_global = QHBoxLayout()
        layout_left = QVBoxLayout()
        layout_left.addWidget(self.toolbar)
        layout_left.addWidget(self.canvas)
        layout_right = QVBoxLayout()
        layout_right.addWidget(self.main_circle)
        layout_right.addWidget(self.circle)
        layout_right.addWidget(self.line)
        layout_right.addWidget(self.button_plot)
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
        self.point_per_line = []                            # точки пересечения маленьких окружностей с линией
        self.style = 1
        # __end of initialization__

        temp = self.main_circle.text().split()
        self.big_circle = []
        self.big_circle.append(int(temp[0]))
        self.big_circle.append(int(temp[1]))
        self.big_circle.append(int(temp[2]))
        temp = self.circle.text().split()
        self.r_small_circle = int(temp[2])
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
        circle = plt.Circle(((self.big_circle[0]), (self.big_circle[1])), radius=(self.big_circle[2]), fill=False)
        circle_for_help = plt.Circle(((self.big_circle[0]), (self.big_circle[1])),
                             radius=(self.big_circle[2]) + self.r_small_circle,
                             fill=False,
                             linestyle='--',
                             color='g')
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
        elif distance <= (2 * self.r_small_circle + self.big_circle[2]):    # дистанция от прямой до центра окружности
                                                # меньше чем диаметр малой окружности + радиус большой окружности
            print("две сопрягающих окружности")
            self.intersection_with_line(2)
        else:
            print("невозможно постоить сопрягающую окружность")
        self.canvas.draw()

    def __plot_line(self, p1, p2):
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
        self.figure.gca().add_line(line)
        self.figure.gca().axis('scaled')
        # self.canvas.draw() #вероятно не нужно
        return first_extreme_point, second_extreme_point

    # def intersection(self, h):
    #     main_circle = self.main_circle.text().split()
    #     koniunkcja_sfer = self.circle.text().split()
    #     r = int(koniunkcja_sfer[2])
    #     R = int(main_circle[2])
    #     o = [int(main_circle[0]), int(main_circle[1])]
    #     line = self.line.text().split()
    #     p1 = [int(line[0]), int(line[1])]
    #     p2 = [int(line[2]), int(line[3])]
    #
    #     oh = [h[0] - o[0], h[1] - o[1]]
    #     print("oh:", oh)
    #     # oh = [o[0] - h[0], o[1] - h[1]]
    #
    #     qv = [p2[0] - p1[0], p2[1] - p1[1]]
    #     print("qv:", qv)
    #     # qv = [p1[0] - p2[0], p1[1] - p2[1]]
    #
    #     b = oh[0]*qv[0] + oh[1]*qv[1]
    #     c = (oh[0]**2)*(qv[0]**2) - (R+r)**2
    #
    #     Px1 = h[0] - (b - (b**2-c)**(1/2))*p2[0]
    #     Py1 = h[1] - (b - (b**2-c)**(1/2))*p2[1]
    #     Px2 = h[0] - (b + (b**2-c)**(1/2))*p2[0]
    #     Py2 = h[1] - (b + (b**2-c)**(1/2))*p2[1]
    #     # print(Px1)
    #     # print(Py1)
    #     # print(Px2)
    #     # print(Py2)
    #
    #     # point1 = mlines.Line2D([Px1, Px1+1], [Py1, Py1+1], color='g')
    #     # point2 = mlines.Line2D([Px2, Px2+1], [Py2, Py2+1], color='g')
    #     # self.figure.gca().add_line(point1)
    #     # self.figure.gca().add_line(point2)

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
                result = self.test(self.extreme_points_of_main_line[0][0],
                                   self.extreme_points_of_main_line[0][1],
                                   self.extreme_points_of_main_line[1][0],
                                   self.extreme_points_of_main_line[1][1],
                                   self.center_of_small_circles[i][0],
                                   self.center_of_small_circles[i][1],
                                   self.r_small_circle + 0.1)
                if result != []:
                    circle = plt.Circle((self.center_of_small_circles[i][0],
                                         self.center_of_small_circles[i][1]),
                                        radius=self.r_small_circle,
                                        fill=False)
                    self.figure.gca().add_patch(circle)
                # res = 0
                # A = Point2D(self.xy[0][0], self.xy[0][1])
                # B = Point2D(self.xy[1][0], self.xy[1][1])
                # F = Segment2D(A, B)
                # C = Point2D(self.point_small_cr[i][0], self.point_small_cr[i][1])
                # print("точки мал окружностей ", self.point_small_cr[i][0], self.point_small_cr[i][1])
                # koniunkcja_sfer = self.circle.text().split()
                # r = int(koniunkcja_sfer[2])
                # circle = plt.Circle((self.point_small_cr[i][0], self.point_small_cr[i][1]), radius=r, fill=False)
                # self.figure.gca().add_patch(circle)
                # c = Circle(C, r)
                # res = c.intersection(F)
                # if res == []:
                #     continue
                # print("result", res)
                # temp1 = res[0]
                # temp2 = res[1]
                # temp1 = str(temp1)[7:]
                # temp2 = str(temp2)[7:]
                # # print(tempu1)
                # # print(temp2)
                # print("RESULT", eval(temp1))
                # print("RESULT", eval(temp2))
            except:
                print("ERROR")

    def test(self, x1, y1, x2, y2, x3, y3, r):
        A = Point2D(x1, y1)
        B = Point2D(x2, y2)
        C = Point2D(x3, y3)
        F = Line2D(A, B)
        # c = Circle(C, sympify(r, rational=True))
        c = Circle(C, sympify(Rational(r), rational=True))
        i_0 = F.intersection(c)
        temp1 = i_0[0]
        temp2 = i_0[1]
        temp1 = str(temp1)[7:]
        temp2 = str(temp2)[7:]
        print("результат теста", eval(temp1), eval(temp2))
        return i_0

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
            first_extreme_point, second_extreme_point = self.__plot_line(p1, p2)
            intersection_points = self.intersection_with_circle(first_extreme_point, second_extreme_point)
            if intersection_points != -666:
                self.center_of_small_circles.append(intersection_points[0])
                self.center_of_small_circles.append(intersection_points[1])
            print("найденные центры малых окружностей прямой №", i, " : ", intersection_points)
            # new_line2 = mlines.Line2D([line_len_r[0], normal_points[0]], [line_len_r[1], normal_points[1]], color='g')
            # self.figure.gca().add_line(new_line2)
        self.__for_debug("конец построения вспомогательных линий")

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec_())
