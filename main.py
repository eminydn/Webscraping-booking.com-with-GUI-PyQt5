import sys
import os
import time
import locale

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QWidget, QFileDialog
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt
import pandas as pd

from app_GUI import Ui_MainWindow
from hotel_application2 import Hotel


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

        self.ui.txtUsername.setText("Facebook kullanıcı adı")
        self.ui.txtPass.setText("Şifre")

        self.ui.dateIn.setDate(QDate.currentDate().addDays(30))
        self.ui.dateOut.setDate(QDate.currentDate().addDays(31))


        #connect
        self.ui.btnSetPath.clicked.connect(self.setPath)
        self.ui.btnRunApp.clicked.connect(self.runApp)


    def trial(self):
        locale.setlocale(locale.LC_ALL, '')
        result = self.ui.dateIn.date().toPyDate()
        gun, ay, yil = result.strftime("%d"), result.strftime("%B"), result.strftime("%Y")
        search_key = f"{str(int(gun))} {ay} {yil}"
        print(search_key)


    def runApp(self):
        email = self.ui.txtUsername.text()
        password = self.ui.txtPass.text()

        self.app = Hotel()
        self.app.sign_in_facebook(email, password)
        time.sleep(15)
        self.app.search(search_key = self.ui.txtCity.text(), search_date = self.setSearchDate())
        self.export_to_excel()


    def setPath(self):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.ui.txtPath.setText(file)
    

    def setSearchDate(self):
        locale.setlocale(locale.LC_ALL, '')
        qt_date = self.ui.dateIn.date().toPyDate()
        gun, ay, yil = qt_date.strftime("%d"), qt_date.strftime("%B"), qt_date.strftime("%Y")
        search_key = f"{str(int(gun))} {ay} {yil}"
        return search_key
    

    def export_to_excel(self):
        df = pd.DataFrame({"Otel ismi":self.app.hotel_names, "Ücret":self.app.prices, "Ek Ücretler":self.app.extra_prices, "Puan":self.app.ratio, "Değerlendirme Sayısı": self.app.ratio_count})
        df.to_excel(f'{self.ui.txtPath.text()}/otel_veri_{self.ui.txtCity.text()}.xlsx')
        print("DONE")




def app():
    app = QtWidgets.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())

app()