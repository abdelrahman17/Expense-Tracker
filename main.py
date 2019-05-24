from UtilitiesMod import *
from mainwindow import *
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from sys import argv, exit


class MainWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.show()


if __name__ == '__main__':
    app = QApplication(argv)
    window = MainWindow()
    exit(app.exec_())
