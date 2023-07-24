import sys
from PyQt5 import QtWidgets, uic
from admin.dashboard import *
from admin.v_jadwal_sidang import *
from admin.mydb import cursor
import hashlib

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("main.ui", self)

        # set alert
        self.msgDialog = QtWidgets.QErrorMessage()

        # Event
        self.submitLogin.clicked.connect(self.aksiLogin)

    def aksiLogin(self):
        username = self.username.text()
        password = self.password.text().encode()
        hash_pw = hashlib.md5(password).hexdigest()

        if username != "" and password != "":
            cursor.execute(
                'SELECT nama, role FROM users WHERE username = "' + username + '" and password = "' + hash_pw + '"')

            result = cursor.fetchone()
            cek = cursor.rowcount

            if cek > 0:

                if result[1] == "admin":
                    self.wdow = Dashboard()
                    self.wdow.show()
                else:
                    self.wdowDosen = JadwalSidang()
                    self.wdowDosen.show()
                self.close()
            else:
                self.msgDialog.showMessage("Username atau Password salah!")
        else:
            self.msgDialog.showMessage("Semua kolom harus diisi!")

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()