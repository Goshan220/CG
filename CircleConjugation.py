import sys
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import pylab
import matplotlib.path


class Window(QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        # buttons
        self.button_plot = QPushButton('Plot')
        self.button_plot.clicked.connect(self.__plot)

        self.main_circle = QLineEdit() #
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
        layout_global.addLayout(layout_left)
        layout_global.addLayout(layout_right)

        self.setLayout(layout_global)
        self.resize(900, 700)

    def __plot(self):
        main_circle = self.main_circle.text().split()
        # circle = self.circle.text().split()
        # line = self.line.text().split()

        self.figure.clear()
        circle = plt.Circle(((int(main_circle[0])), (int(main_circle[1]))), radius=(int(main_circle[2])), fill=False)
        self.figure.gca().add_patch(circle)
        self.figure.gca().axis('scaled')
        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec_())
