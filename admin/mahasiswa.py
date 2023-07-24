import sys
from PyQt5 import QtWidgets, uic
from admin.mydb import *
from admin.mydb import cursor


class Mahasiswa(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("admin/mahasiswa.ui", self)
        
        # self.inptID.setReadOnly(True)

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
        self.selectFak()

        # btnFrm
        self.disableBtn()
        pass

    def selectFak(self):
        cursor.execute("SELECT kode, nama FROM fakultas")

        data = cursor.fetchall()

        self.inptFak.clear()
        no = 0;
        for item_name in data:
            self.inptFak.addItem(item_name[0]+" - "+item_name[1])
            self.inptFak.setItemData(no, item_name[0])
            no += 1

    def saveData(self):
        nim = self.inptNim.text()
        nama = self.inptNama.text()
        jk = self.inptJk.currentText()
        kodeFak = self.inptFak.currentData()
        nohp = self.inptHp.text()

        if nama != "" and jk != "" and kodeFak != "" and nohp != "":
            query = "INSERT INTO mahasiswa (nim, nama, jk, kodeFak, nohp) VALUES(%s, %s, %s, %s, %s)"
            value = (nim, nama, jk, kodeFak, nohp)

            try:

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
        query = "SELECT * FROM mahasiswa"
        cursor.execute(query)
        result = cursor.fetchall()

        row = 0
        self.tableData.setRowCount(len(result))

        for data in result:
            self.tableData.setItem(
                row, 0, QtWidgets.QTableWidgetItem(str(data[0])))
            self.tableData.setItem(
                row, 1, QtWidgets.QTableWidgetItem(str(data[1])))
            self.tableData.setItem(
                row, 2, QtWidgets.QTableWidgetItem(str(data[2])))
            self.tableData.setItem(
                row, 3, QtWidgets.QTableWidgetItem(str(data[3])))
            self.tableData.setItem(
                row, 4, QtWidgets.QTableWidgetItem("0"+str(data[4])))
            row = row+1


    def getData(self):
        row = self.tableData.currentRow()
        
        nim = self.tableData.item(row, 0).text()

        query = "SELECT * FROM mahasiswa INNER JOIN fakultas ON mahasiswa.kodeFak=fakultas.kode WHERE mahasiswa.nim = '"+nim+"'"
        cursor.execute(query)
        result = cursor.fetchone()

        nama = result[1]
        jk = result[2]
        kodeFak = result[3]
        noHp = result[4]
        namaFak = result[6]

        self.inptNim.setText(nim)
        self.inptNim.setReadOnly(True)
        self.inptNama.setText(nama)
        self.inptJk.setCurrentText(jk)

        self.inptFak.setCurrentText(kodeFak+" - "+namaFak)
        
        self.inptHp.setText(str(noHp))

        self.enableBtn()
        self.btnSave.setEnabled(False)

    def updateData(self):
        nim = self.inptNim.text()
        nama = self.inptNama.text()
        jk = self.inptJk.currentText()
        kodeFak = self.inptFak.currentData()
        nohp = self.inptHp.text()

        if nama != "" and jk != "" and kodeFak != "" and nohp != "":
            query = "UPDATE mahasiswa SET nama ='" + nama + "', jk ='" + jk + "', kodeFak ='" + kodeFak + "', nohp ='" + nohp + "' WHERE nim ='" + nim + "' "
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
        nim = self.inptNim.text()
        try:
            query = "DELETE FROM mahasiswa WHERE nim = '" + nim + "'"
            cursor.execute(query)
            mydb.commit()
            self.msgDialog.showMessage("Berhasil dihapus")
            self.loadData()
            self.resetFrm()
        except:
            self.msgDialog.showMessage("Gagal!")

    def resetFrm(self):
        self.inptNim.setText("")
        self.inptNim.setReadOnly(False)
        self.inptNama.setText("")
        self.inptHp.setText("")
        self.disableBtn()
        self.btnSave.setEnabled(True)

    def disableBtn(self):
        self.btnDelete.setEnabled(False)
        self.btnUpdate.setEnabled(False)

    def enableBtn(self):
        self.btnDelete.setEnabled(True)
        self.btnUpdate.setEnabled(True)
