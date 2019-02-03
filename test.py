import sys
from PyQt5 import QtWidgets, uic

qtCreatorFile = "iot_main.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.btn_ok.clicked.connect(self.copy)

    def copy(self):
        old_string = self.result_txt.toPlainText()
        new_string = "Copied:\t"+ self.input_txt.toPlainText()

        self.result_txt.setText((old_string+"\n" if old_string!="" else "") + new_string)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
