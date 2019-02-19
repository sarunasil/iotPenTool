import sys
import subprocess
from PyQt5 import QtWidgets, uic
import time

qtCreatorFile = "iot_main.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        pushButton = QtWidgets.QPushButton("Dynamic button", self)
        # pushButton.setGeometry(100,100,100,100)

        # layout = QtWidgets.QHBoxLayout()
        # layout.addWidget(pushButton)
        # self.setLayout(layout)

        self.btn_ok.clicked.connect(self.execute_test)

    def execute(self, cmd, arg):
        process = subprocess.Popen(
            [cmd, arg] if arg else [cmd], 
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return process.communicate()

    def execute_test(self):
        cmd_input_string = str(self.cmd_input_txt.toPlainText())
        arg_input_string = str(self.arg_input_txt.toPlainText())


        result, error = self.execute(cmd_input_string, arg_input_string)


        self.result_txt.append(40*'-')
        for line in result.decode().split('\\n'):
            self.result_txt.append(line)

        self.error_txt.append(40*'-')
        for line in error.decode().split('\\n'):
            self.error_txt.append(line)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
