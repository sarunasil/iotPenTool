from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("MainWindow")
        MainWindow.resize(200, 200)
        # MainWindow.setFixedSize(200,200)
        # MainWindow.setMaximumHeight(200)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        scroll = QtWidgets.QScrollArea()
        scroll_widget = QtWidgets.QWidget()
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        widget_layout = QtWidgets.QVBoxLayout()
        widget_layout.addWidget(QtWidgets.QPushButton("TEstas"))
        widget_layout.addWidget(QtWidgets.QPushButton("TEstas2"))
        widget_layout.addWidget(QtWidgets.QPushButton("TEstas3"))
        widget_layout.addWidget(QtWidgets.QPushButton("TEstas "))
        widget_layout.addWidget(QtWidgets.QPushButton("TEstas22"))
        widget_layout.addWidget(QtWidgets.QPushButton("TEstas33"))
        widget_layout.addWidget(QtWidgets.QPushButton("TEstas  "))
        widget_layout.addWidget(QtWidgets.QPushButton("TEstas222"))
        widget_layout.addWidget(QtWidgets.QPushButton("TEstas333"))
        widget_layout.addWidget(QtWidgets.QPushButton("TEstas    "))
        widget_layout.addWidget(QtWidgets.QPushButton("TEstas22222"))
        widget_layout.addWidget(QtWidgets.QPushButton("TEstas33333"))
        scroll_widget.setLayout(widget_layout)


        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(scroll)
        self.centralwidget.setLayout(self.layout)

        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

class Window(QtWidgets.QMainWindow):
    resized = QtCore.pyqtSignal()
    def  __init__(self, parent=None):
        super(Window, self).__init__(parent=parent)
        ui = Ui_MainWindow()
        ui.setupUi(self)
        self.resized.connect(self.someFunction)

    def resizeEvent(self, event):
        self.resized.emit()
        return super(Window, self).resizeEvent(event)

    def someFunction(self):
        print(self.size())


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())