import sys
from PyQt5 import QtWidgets, uic
from admin.mydb import *
from admin.mydb import cursor


class Prodi(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("admin/prodi.ui", self)
        
        # set alert
        self.msgDialog = QtWidgets.QErrorMessage()

        # Event
        self.btnSave.clicked.connect(self.saveData)
        self.btnUpdate.clicked.connect(self.updateData)
        self.btnDelete.clicked.connect(self.deleteData)
        self.btnReset.clicked.connect(self.resetFrm)
        self.tableData.clicked.connect(self.getData)

        # Data
        self.loadData()

        # btnFrm
        self.disableBtn()
        pass

    def saveData(self):
        kode = self.inptKode.text()
        nama = self.inptNama.text()

        if kode != "" and nama != "":

            try:
                query = "INSERT INTO fakultas (kode, nama) VALUES(%s, %s)"
                value = (kode, nama)

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
        query = "SELECT kode, nama FROM fakultas"
        cursor.execute(query)
        result = cursor.fetchall()

        row = 0
        self.tableData.setRowCount(len(result))

        for data in result:
            self.tableData.setItem(
                row, 0, QtWidgets.QTableWidgetItem(str(data[0])))
            self.tableData.setItem(
                row, 1, QtWidgets.QTableWidgetItem(str(data[1])))
            row = row+1


    def getData(self):
        row = self.tableData.currentRow()

        dataKode = self.tableData.item(row, 0).text()
        dataNama = self.tableData.item(row, 1).text()

        self.inptKode.setText(dataKode)
        self.inptKode.setReadOnly(True)
        self.inptNama.setText(dataNama)

        self.enableBtn()
        self.btnSave.setEnabled(False)

    def updateData(self):
        kode = self.inptKode.text()
        nama = self.inptNama.text()

        if kode != "" and nama != "":
            query = "UPDATE fakultas SET kode ='" + kode + "', nama ='" + nama + "' WHERE kode ='" + kode + "' "
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
        kode = self.inptKode.text()
        try:
            query = "DELETE FROM fakultas WHERE kode = '" + kode + "'"
            cursor.execute(query)
            mydb.commit()
            self.msgDialog.showMessage("Berhasil dihapus")
            self.loadData()
            self.resetFrm()
        except:
            self.msgDialog.showMessage("Gagal!")

    def resetFrm(self):
        self.inptKode.setText("")
        self.inptKode.setReadOnly(False)
        self.inptNama.setText("")
        self.disableBtn()
        self.btnSave.setEnabled(True)

    def disableBtn(self):
        self.btnDelete.setEnabled(False)
        self.btnUpdate.setEnabled(False)

    def enableBtn(self):
        self.btnDelete.setEnabled(True)
        self.btnUpdate.setEnabled(True)
