# Тест самопересечения и самокасания полигона (self_test).

import matplotlib.pyplot as plt

def funcinput(points):
    # points = [(0,0), (1,0), (2,0.5), (1,1), (1,2)]
    # points = [(0,0), (0.5, 0), (-0.5, 0.5), (0.5, 1), (0, 2)]
    # points = [(0,0), (1, 0), (0, 1), (1, 2), (0, 2)]
    # points = [(0,0), (0.5, 0), (-0.5, 0.5)]
    # points = [(0,0), (0.5, 0), (-0.5, 0.5), (0.5, 1)]
    # points = [(0,0), (0.5, 0), (0.5, 1), (-0.5, 0.5)]

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
    print(points)
    return points


def getNf2(a, b, c):
    """
    There are 3 points: А(х1,у1), Б(х2,у2), С(х3,у3).
    D = (х3 - х1) * (у2 - у1) - (у3 - у1) * (х2 - х1)
     - If D = 0 - then, point С is on АБ.
     - If D < 0 - then, point С to the left of a straight line.
     - If D > 0 - then, point С to the right of a straight line.
    """
    return (c[0] - a[0]) * (b[1] - a[1]) - (c[1] - a[1]) * (b[0] - a[0])


def self_test(testing, points): #testing 1 = самопересечение 2 = самокасание
    """
    :param testing: 1 - самопересечение, 2 - самокасание
    :param points: - вершины полигона
    :return: 1 - есть пересечение, 0 - нет
    """
    print (len(points))
    n = len(points) - 1
    print("Используется N = ", n )
    if n <= 3 :
        return 0
    else:
        for i in range(n-2):
            print ("I: ", i)
            if i == 0 : # или 1 ?!?
                sublen = n - 1
            else:
                sublen = n
            for j in range(i+2, sublen):
                print("J: ", j)
                a = getNf2(points[i], points[i + 1], points[j])
                b = getNf2(points[i], points[i + 1], points[j + 1])
                c = getNf2(points[j], points[j + 1], points[i])
                d = getNf2(points[j], points[j + 1], points[i + 1])
                print( "A: ", a , " B: ", b , " C: ", c , " D: ", d )
                if testing == 1:
                    if a != b :
                        print ("A=B")
                    else:
                        continue
                    if a*b < 0 :
                        print("AB < 0")
                    else:
                        continue
                    if c*d < 0 :
                        return 1
                    else:
                        continue
                if testing == 2:
                    if a != b :
                        print ("A=B")
                    else:
                        continue
                    if ((a*b <= 0)&(c*d==0))|((a*b==0)&(c*d<=0)):
                        return 1
                    else:
                        continue
        return 0


def __main__():
    points = []
    points = funcinput(points)

    plt.figure(1)
    plt.subplot(111)
    x0 = []
    y0 = []

    for i in points:
        x0.append(i[0])
        y0.append(i[1])

    plt.plot(x0, y0)
    self_kos = self_test(2, points)
    self_per = self_test(1, points)

    if self_kos == 1:
        plt.plot(' ', label='касание')
    else:
        plt.plot(' ', label='касания нет')

    if self_per == 1:
        plt.plot(' ', label='пересечение')
    else:
        plt.plot(' ', label='пересечения нет')

    plt.legend(loc='best', shadow=True)
    plt.show()


__main__()
