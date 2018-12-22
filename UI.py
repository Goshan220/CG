
from SelfIntersection import SelfIntersection
import sys
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt


class Window(QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        # buttons
        self.button_plot = QPushButton('Plot')
        self.button_plot.clicked.connect(self.__user_input)
        self.button_add = QPushButton('Add')
        self.button_add.clicked.connect(self.__add)
        self.button_rem = QPushButton('Remove')
        self.button_rem.clicked.connect(self.__rem)
        self.button_rand = QPushButton('Random')
        self.button_rand.clicked.connect(self.__rand)
        self.button_up = QPushButton('UP')
        self.button_up.clicked.connect(self.__up)
        self.button_down = QPushButton('DOWN')
        self.button_down.clicked.connect(self.__down)

        self.list_view = QListWidget()
        self.line_edit = QLineEdit()

        self.check_box_1 = QCheckBox("Самокосание")
        self.check_box_2 = QCheckBox("Самопересечие")
        self.check_box_1.setDisabled(1)
        self.check_box_2.setDisabled(1)

        layout_global = QHBoxLayout()
        layout_left = QVBoxLayout()
        layout_left.addWidget(self.toolbar)
        layout_left.addWidget(self.canvas)
        layout_left.addWidget(self.check_box_1)
        layout_left.addWidget(self.check_box_2)
        layout_right = QVBoxLayout()
        layout_right.addWidget(self.list_view)
        layout_right.addWidget(self.line_edit)
        layout_right_buttons1 = QHBoxLayout()
        layout_right_buttons2 = QHBoxLayout()
        layout_right_buttons1.addWidget(self.button_add)
        layout_right_buttons1.addWidget(self.button_up)
        layout_right_buttons1.addWidget(self.button_plot)
        layout_right_buttons2.addWidget(self.button_rem)
        layout_right_buttons2.addWidget(self.button_down)
        layout_right_buttons2.addWidget(self.button_rand)
        layout_right.addLayout(layout_right_buttons1)
        layout_right.addLayout(layout_right_buttons2)
        layout_global.addLayout(layout_left)
        layout_global.addLayout(layout_right)

        self.setLayout(layout_global)
        self.resize(900, 700)

    def __user_input(self):
        si = SelfIntersection()
        users_input = []
        for index in range(self.list_view.count()):
            users_input.append(self.list_view.item(index).text())
        print(users_input)
        t = si.start(2, users_input)
        print(t)
        self.__plot(t)

    def __plot(self, data):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.axes.set_aspect('equal') #чтобы соотношение осей было верным
        ax.plot(data[0], data[1], 'o-')
        self.canvas.draw()
        if data[2] == 1:
            self.check_box_1.setChecked(1)
        else:
            self.check_box_1.setChecked(0)
        if data[3] == 1:
            self.check_box_2.setChecked(1)
        else:
            self.check_box_2.setChecked(0)

    def __add(self):
        text = self.line_edit.text()
        self.list_view.addItem(text)
        self.line_edit.setText("")
        if len(text.split()) > 1:
            self.__user_input()

    def __rem(self):
        list_items = self.list_view.selectedItems()
        if not list_items:
            return
        for item in list_items:
            self.list_view.takeItem(self.list_view.row(item))

    def __up(self):
        current_row = self.list_view.currentRow()
        current_item = self.list_view.takeItem(current_row)
        self.list_view.insertItem(current_row - 1, current_item)

    def __down(self):
        current_row = self.list_view.currentRow()
        current_item = self.list_view.takeItem(current_row)
        self.list_view.insertItem(current_row + 1, current_item)

    def __rand(self):
        si = SelfIntersection()
        users_input = []
        for index in range(self.list_view.count()):
            users_input.append(self.list_view.item(index).text())
        print(users_input)
        if len(users_input) == 1:
            t = si.start(1, users_input)
            print(t)
            self.__plot(t)
        else:
            self.list_view.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec_())
