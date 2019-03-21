
#Shamelessly taken from
#https://stackoverflow.com/questions/51230544/pyqt5-how-to-set-tabwidget-west-but-keep-the-text-horizontal/51230694#51230694

from PyQt5 import QtCore, QtGui, QtWidgets
class TabBar(QtWidgets.QTabBar):
    def __init__(self, direction):
        super().__init__()

        self.direction = direction

    def tabSizeHint(self, index):
        s = QtWidgets.QTabBar.tabSizeHint(self, index)
        s.transpose()
        return s

    def paintEvent(self, event):
        painter = QtWidgets.QStylePainter(self)
        opt = QtWidgets.QStyleOptionTab()

        for i in range(self.count()):
            self.initStyleOption(opt, i)
            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabShape, opt)
            painter.save()

            s = opt.rect.size()
            s.transpose()
            r = QtCore.QRect(QtCore.QPoint(), s)
            r.moveCenter(opt.rect.center())
            opt.rect = r

            c = self.tabRect(i).center()
            painter.translate(c)
            if self.direction == QtWidgets.QTabWidget.West:
                painter.rotate(90)
            elif self.direction == QtWidgets.QTabWidget.East:
                painter.rotate(270)
            painter.translate(-c)
            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabLabel, opt);
            painter.restore()


class TabWidget(QtWidgets.QTabWidget):
    def __init__(self, direction=QtWidgets.QTabWidget.West, *args, **kwargs):
        QtWidgets.QTabWidget.__init__(self, *args, **kwargs)
        self.setTabBar(TabBar(direction))
        self.setTabPosition(direction)


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = TabWidget()
    w.addTab(QtWidgets.QWidget(), "tab1")
    w.addTab(QtWidgets.QWidget(), "tab2")
    w.addTab(QtWidgets.QWidget(), "tab3")
    w.show()

    sys.exit(app.exec_())