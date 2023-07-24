import sys
from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore
from admin.mydb import *
from admin.mydb import cursor


class Sidang(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("admin/sidang.ui", self)

        tanggal = "01/01/2023"
        widgetDate = QtCore.QDate.fromString(tanggal, "dd/MM/yyyy")

        self.inptID.setReadOnly(True)
        self.inptJadwal.setDate(widgetDate)

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
        self.selectMhs()
        self.selectDosen()

        # btnFrm
        self.disableBtn()
        pass

    def selectMhs(self):
        cursor.execute("SELECT nim, nama, kodeFak FROM mahasiswa")

        data = cursor.fetchall()

        self.inptMhs.clear()
        no = 0;
        for item_name in data:
            self.inptMhs.addItem(item_name[2]+" - "+item_name[1])
            self.inptMhs.setItemData(no, item_name[0])
            no += 1

    def selectDosen(self):
        cursor.execute("SELECT username, nama FROM users WHERE role = 'dosen'")

        data = cursor.fetchall()

        self.inptDosen.clear()
        no = 0;
        for item_name in data:
            self.inptDosen.addItem(item_name[1])
            self.inptDosen.setItemData(no, item_name[0])
            no += 1

    def saveData(self):
        judul = self.inptJudul.text()
        tanggal = self.inptJadwal.date()
        jadwal = tanggal.toString("dd/MM/yyyy")
        mhsNim = self.inptMhs.currentData()
        dosen = self.inptDosen.currentData()

        if judul != "" and jadwal != "" and mhsNim != "" and dosen != "":

            cursor.execute("SELECT judul, jadwal FROM sidang WHERE judul = '"+judul+"' or jadwal = '"+jadwal+"'")
            cursor.fetchone()
            cek = cursor.rowcount

            if cek < 1:
                query = "INSERT INTO sidang (judul, jadwal, mhsNim, dosen) VALUES(%s, %s, %s, %s)"
                value = (judul, jadwal, mhsNim, dosen)

                try:
                    cursor.execute(query, value)
                    mydb.commit()

                    self.msgDialog.showMessage("Berhasil disimpan")
                    self.loadData()
                    self.resetFrm()
                except:
                    self.msgDialog.showMessage("Gagal!")
            else:
                self.msgDialog.showMessage("Judul skripsi atau jadwal sudah sudah ada!")
        else:
            self.msgDialog.showMessage("Semua kolom harus diisi!")

    def loadData(self):
        query = "SELECT sidang.id, sidang.judul, sidang.jadwal, mahasiswa.nama, users.nama FROM sidang INNER JOIN mahasiswa ON sidang.mhsNim = mahasiswa.nim INNER JOIN users ON sidang.dosen = users.username"
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
                row, 4, QtWidgets.QTableWidgetItem(str(data[4])))
            row = row+1

    def getData(self):
        row = self.tableData.currentRow()
        
        id = self.tableData.item(row, 0).text()

        query = "SELECT sidang.id, sidang.judul, sidang.jadwal, mahasiswa.kodeFak, mahasiswa.nama, users.nama FROM sidang INNER JOIN mahasiswa ON sidang.mhsNim = mahasiswa.nim INNER JOIN users ON sidang.dosen = users.username WHERE sidang.id = '"+id+"'"
        cursor.execute(query)
        result = cursor.fetchone()

        judul = result[1]
        jadwal = result[2]
        kodeFak = result[3]
        namaMhs = result[4]
        namaDosen = result[5]

        self.inptID.setText(id)
        self.inptJudul.setText(judul)
        self.inptJadwal.setDate(QtCore.QDate.fromString(jadwal, "dd/MM/yyyy"))
        
        self.inptMhs.setCurrentText(kodeFak+" - "+namaMhs)
        self.inptDosen.setCurrentText(namaDosen)
        
        self.enableBtn()
        self.btnSave.setEnabled(False)

    def updateData(self):
        id = self.inptID.text()
        judul = self.inptJudul.text()
        tanggal = self.inptJadwal.date()
        jadwal = tanggal.toString("dd/MM/yyyy")
        mhsNim = self.inptMhs.currentData()
        dosen = self.inptDosen.currentData()

        if judul != "" and jadwal != "" and mhsNim != "" and dosen != "":
            cursor.execute("SELECT judul, jadwal FROM sidang WHERE (judul = '"+judul+"' or jadwal = '"+jadwal+"') and id != '"+id+"'")
            cursor.fetchone()
            cek = cursor.rowcount

            if cek < 1:
                query = "UPDATE sidang SET judul ='" + judul + "', jadwal ='" + jadwal + "', mhsNim ='" + str(mhsNim) + "', dosen ='" + dosen + "' WHERE id ='" + id + "' "
                try:

                    cursor.execute(query)
                    mydb.commit()

                    self.loadData()
                    self.resetFrm()

                    self.msgDialog.showMessage("Berhasil disimpan")
                except:
                    self.msgDialog.showMessage("Gagal!")
            else:
                self.msgDialog.showMessage("Judul skripsi atau jadwal sudah sudah ada!")
        else:
            self.msgDialog.showMessage("Semua kolom harus diisi!")

    def deleteData(self):
        id = self.inptID.text()
        try:
            query = "DELETE FROM sidang WHERE id = '" + id + "'"
            cursor.execute(query)
            mydb.commit()
            self.msgDialog.showMessage("Berhasil dihapus")
            self.loadData()
            self.resetFrm()
        except:
            self.msgDialog.showMessage("Gagal!")

    def resetFrm(self):
        self.inptID.setText("")
        self.inptJudul.setText("")
        # self.inptJadwal.setText("01/01/2023")
        self.disableBtn()
        self.btnSave.setEnabled(True)

    def disableBtn(self):
        self.btnDelete.setEnabled(False)
        self.btnUpdate.setEnabled(False)

    def enableBtn(self):
        self.btnDelete.setEnabled(True)
        self.btnUpdate.setEnabled(True)