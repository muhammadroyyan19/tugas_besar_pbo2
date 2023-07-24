import sys
from PyQt5 import QtWidgets, uic
from admin.mydb import *
from admin.mydb import cursor
import hashlib


class Dosen(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("admin/dosen.ui", self)
        
        # set alert
        self.msgDialog = QtWidgets.QErrorMessage()

        # Event
        self.btnSave.clicked.connect(self.saveData)
        self.btnUpdate.clicked.connect(self.updateData)
        self.btnDelete.clicked.connect(self.deleteData)
        self.btnReset.clicked.connect(self.resetFrm)
        self.tableDosen.clicked.connect(self.getData)

        # Data
        self.loadData()

        # btnFrm
        self.disableBtn()
        pass

    def saveData(self):
        nama = self.inptNama.text()
        username = self.inptUsername.text()
        password = self.inptPassword.text().encode()
        hash_pw = hashlib.md5(password).hexdigest()
        jk = self.inptJk.currentText()
        email = self.inptEmail.text()
        nohp = self.inptNohp.text()
        role = "dosen"

        if nama != "" and username != "" and password != "" and jk != "" and email != "" and nohp != "":

            try:
                query = "INSERT INTO users (username, nama, password, jk, email, nohp, role) VALUES(%s, %s, %s, %s, %s, %s, %s)"
                value = (username, nama, hash_pw, jk, email, nohp, role)

                cursor.execute(query, value)
                mydb.commit()

                self.msgDialog.showMessage("Berhasil disimpan")
                self.loadData()
                self.resetFrm()
            except:
                self.msgDialog.showMessage("Gagal!")
        else:
            self.msgDialog.showMessage("Semua kolom harus diisi!")
            
    def loadData(self):
        query = "SELECT username, nama, jk, email, nohp FROM users WHERE role = 'dosen'"
        cursor.execute(query)
        result = cursor.fetchall()

        row = 0
        self.tableDosen.setRowCount(len(result))

        for data in result:
            self.tableDosen.setItem(
                row, 0, QtWidgets.QTableWidgetItem(str(data[0])))
            self.tableDosen.setItem(
                row, 1, QtWidgets.QTableWidgetItem(str(data[1])))
            self.tableDosen.setItem(
                row, 2, QtWidgets.QTableWidgetItem(str(data[2])))
            self.tableDosen.setItem(
                row, 3, QtWidgets.QTableWidgetItem(str(data[3])))
            self.tableDosen.setItem(
                row, 4, QtWidgets.QTableWidgetItem("0"+str(data[4])))
            row = row+1


    def getData(self):
        row = self.tableDosen.currentRow()

        dataUsername = self.tableDosen.item(row, 0).text()
        dataNama = self.tableDosen.item(row, 1).text()
        # dataPassword = self.tableDosen.item(row, 0).text()
        dataJk = self.tableDosen.item(row, 2).text()
        dataEmail = self.tableDosen.item(row, 3).text()
        dataHp = self.tableDosen.item(row, 4).text()

        self.inptUsername.setText(dataUsername)
        self.inptUsername.setReadOnly(True)
        self.inptNama.setText(dataNama)
        self.inptPassword.setText("")
        self.inptJk.setCurrentText(dataJk)
        self.inptEmail.setText(dataEmail)
        self.inptNohp.setText("0"+dataHp)

        self.enableBtn()
        self.btnSave.setEnabled(False)

    def updateData(self):
        nama = self.inptNama.text()
        username = self.inptUsername.text()
        password = self.inptPassword.text().encode()
        hash_pw = hashlib.md5(password).hexdigest()
        jk = self.inptJk.currentText()
        email = self.inptEmail.text()
        nohp = self.inptNohp.text()

        if nama != "" and jk != "" and email != "" and nohp != "":
            if len(password) > 0:
                query = "UPDATE users SET nama ='" + nama + "', password ='" + hash_pw + "', jk ='" + jk + "', email ='" + email + "', nohp ='" + nohp + "' WHERE username = '" + username + "' "
            else:
                query = "UPDATE users SET nama ='" + nama + "', jk ='" + jk + "', email ='" + email + "', nohp ='" + nohp + "' WHERE username ='" + username + "' "
            try:

                cursor.execute(query)
                mydb.commit()

                self.loadData()
                self.resetFrm()

                self.msgDialog.showMessage("Berhasil disimpan")
            except:
                self.msgDialog.showMessage("Gagal!")
        else:
            self.msgDialog.showMessage("Semua kolom harus diisi!")

    def deleteData(self):
        username = self.inptUsername.text()
        try:
            query = "DELETE FROM users WHERE username = '" + username + "'"
            cursor.execute(query)
            mydb.commit()
            self.msgDialog.showMessage("Berhasil dihapus")
            self.loadData()
            self.resetFrm()
        except:
            self.msgDialog.showMessage("Gagal!")



    def resetFrm(self):
        self.inptNama.setText("")
        self.inptUsername.setText("")
        self.inptUsername.setReadOnly(False)
        self.inptPassword.setText("")
        self.inptEmail.setText("")
        self.inptNohp.setText("")
        self.disableBtn()
        self.btnSave.setEnabled(True)

    def disableBtn(self):
        self.btnDelete.setEnabled(False)
        self.btnUpdate.setEnabled(False)

    def enableBtn(self):
        self.btnDelete.setEnabled(True)
        self.btnUpdate.setEnabled(True)
