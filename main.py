import sys
import os
import time
import locale

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QWidget, QFileDialog
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt
import pandas as pd

from app_GUI import Ui_MainWindow
from hotel_application_v2 import Hotel


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #variables
        self.currentPath = os.getcwd().replace('\\', '/')


        #set Properties
        self.setWindowTitle("Booking.com WebScraper")
        self.ui.txtPath.setText(self.currentPath)
        self.ui.spnRoom.setMinimum(1)
        self.ui.spnAdult.setMinimum(1)

        # self.ui.txtUsername.setText("Facebook kullanıcı adı")
        # self.ui.txtPass.setText("Şifre")

        self.ui.txtUsername.setText("Kullanıcı adı")
        self.ui.txtPass.setText("Şifre")

        self.ui.dateIn.setDate(QDate.currentDate().addDays(30))
        self.ui.dateOut.setDate(QDate.currentDate().addDays(31))


        #connect
        self.ui.btnSetPath.clicked.connect(self.setPath)
        self.ui.btnRunApp.clicked.connect(self.runApp)


    def trial(self):
        locale.setlocale(locale.LC_ALL, '')
        result = self.ui.dateIn.date().toPyDate()
        gun, ay, yil = result.strftime( "%d"), result.strftime("%B"), result.strftime("%Y")
        search_key = f"{str(int(gun))} {ay} {yil}"
        print(search_key)


    def runApp(self):
        email = self.ui.txtUsername.text()
        password = self.ui.txtPass.text()

        adult = self.ui.spnAdult.value()
        children = self.ui.spnChildren.value()
        room = self.ui.spnRoom.value()

        self.app = Hotel()
        self.app.sign_in_facebook(email, password)
        self.app.change_currency()

        if adult != 2 or children != 0 or room != 1:
            self.app.set_room_type(adult, children, room)

        self.app.search(search_key = self.ui.txtCity.text(), search_date = self.setSearchDate())

        excel_dateIn = self.ui.dateIn.date().toPyDate().strftime("%d-%m-%Y")
        excel_dateOut = self.ui.dateOut.date().toPyDate().strftime("%d-%m-%Y")

        self.app.export_to_excel(self.ui.txtPath.text(), self.ui.txtCity.text(), room_selection=[adult,children,room], check_in_out=[excel_dateIn, excel_dateOut])
        self.app.browser.close()


    def setPath(self):
        try:
            file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
            self.ui.txtPath.setText(file)
        except:
            print("Path can't be changed")


    def setSearchDate(self):
        locale.setlocale(locale.LC_ALL, '')
        qt_date = self.ui.dateIn.date().toPyDate()
        day, month, year = qt_date.strftime("%d"), qt_date.strftime("%B"), qt_date.strftime("%Y")
        search_key = f"{str(int(day))} {month} {year}"
        return search_key
    

def app():
    app = QtWidgets.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())

app()