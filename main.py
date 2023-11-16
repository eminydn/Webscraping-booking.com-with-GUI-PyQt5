import sys
import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QWidget, QFileDialog

from app_GUI import Ui_MainWindow
from hotel_application import Hotel

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #variables
        self.currentPath = os.getcwd().replace('\\', '/')

        #connect
        self.ui.btnSetPath.clicked.connect(self.setPath)

        #set Properties
        self.ui.txtPath.setText(self.currentPath)

        self.app = Hotel()
        self.app()

    def setPath(self):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.ui.txtPath.setText(file)



def app():
    app = QtWidgets.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())

app()