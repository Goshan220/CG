import random


class SelfIntersection:
    def start(self, key=0, users_input=None):
        """
        :param key: 1 - random points, 0 - users points, 2 - GUI
        :param users_input: users input from GUI
        :return: points
        """
        points = []

        if key == 0:
            print("Input vertices of a polygon. For exit write your first point.")
            i = 0
            while True:
                x, y = input("Please, write point:  ").split()
                x = int(x)
                y = int(y)
                if i != 0 and x == points[0][0] and y == points[0][1]:
                    break
                points.append((x, y))
                i += 1
            i = 0
            for p in points:
                print("Point " + str(i) + ": " + str(p[0]) + ", " + str(p[1]))
                i += 1
            points.append(points[0])
            result = self.__testing(points)
            return result

        if key == 1:
            number = int(users_input[0])
            print(number)
            for i in range(number):
                x = int(random.randint(0, 20))
                y = int(random.randint(0, 20))
                points.append((x, y))
            points.append(points[0])
            result = self.__testing(points)
            return result

        if key == 2:
            if len(users_input) == 0:
                points.append((0, 0))
            print("Users input", users_input)
            for i in range(len(users_input)):
                temp = str(users_input[i]).split()
                x = int(temp[0])
                y = int(temp[1])
                points.append((x, y))
            points.append(points[0])
            result = self.__testing(points)
            return result

    def __get_nf2(self, a, b, c):
        """
        There are 3 points: А(х1,у1), Б(х2,у2), С(х3,у3).
        D = (х3 - х1) * (у2 - у1) - (у3 - у1) * (х2 - х1)
         - If D = 0 - then, point С is on АБ.
         - If D < 0 - then, point С to the left of a straight line.
         - If D > 0 - then, point С to the right of a straight line.
        """
        return (c[0] - a[0]) * (b[1] - a[1]) - (c[1] - a[1]) * (b[0] - a[0])

    def __self_test(self, testing, points):  # testing 1 = самопересечение 2 = самокасание
        """
        :param testing: 1 - самопересечение, 2 - самокасание
        :param points: - вершины полигона
        :return: 1 - есть пересечение, 0 - нет
        """
        print(len(points))
        n = len(points) - 1
        print("Используется N = ", n)
        if n <= 3:
            return 0
        else:
            for i in range(n - 2):
                print("I: ", i)
                if i == 0:  # или 1 ?!?
                    sublen = n - 1
                else:
                    sublen = n
                for j in range(i + 2, sublen):
                    print("J: ", j)
                    a = self.__get_nf2(points[i], points[i + 1], points[j])
                    b = self.__get_nf2(points[i], points[i + 1], points[j + 1])
                    c = self.__get_nf2(points[j], points[j + 1], points[i])
                    d = self.__get_nf2(points[j], points[j + 1], points[i + 1])
                    print("A: ", a, " B: ", b, " C: ", c, " D: ", d)
                    if testing == 1:
                        if a != b:
                            print("A=B")
                        else:
                            continue
                        if a * b < 0:
                            print("AB < 0")
                        else:
                            continue
                        if c * d < 0:
                            return 1
                        else:
                            continue
                    if testing == 2:
                        if a != b:
                            print("A=B")
                        else:
                            continue
                        if ((a * b <= 0) & (c * d == 0)) | ((a * b == 0) & (c * d <= 0)):
                            return 1
                        else:
                            continue
            return 0

    def __testing(self, points):
        x0 = []
        y0 = []
        for i in points:
            x0.append(i[0])
            y0.append(i[1])
        self_per = self.__self_test(1, points)
        self_kos = self.__self_test(2, points)
        return x0, y0, self_kos, self_per
