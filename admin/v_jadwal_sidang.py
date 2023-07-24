import sys
from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore
from admin.mydb import *
from admin.mydb import cursor


class JadwalSidang(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("admin/v_jadwal_sidang.ui", self)
        self.loadData()

    def loadData(self):
        query = "SELECT mahasiswa.nama, mahasiswa.kodeFak, fakultas.nama, sidang.judul, sidang.jadwal, users.nama FROM sidang INNER JOIN mahasiswa ON sidang.mhsNim = mahasiswa.nim INNER JOIN fakultas ON mahasiswa.kodeFak = fakultas.kode INNER JOIN users ON sidang.dosen = users.username"
        cursor.execute(query)
        result = cursor.fetchall()

        row = 0
        self.tableData.setRowCount(len(result))

        for data in result:
            self.tableData.setItem(
                row, 0, QtWidgets.QTableWidgetItem(str(data[0])))
            self.tableData.setItem(
                row, 1, QtWidgets.QTableWidgetItem(str(data[1])+" - "+str(data[2])))
            self.tableData.setItem(
                row, 2, QtWidgets.QTableWidgetItem(str(data[3])))
            self.tableData.setItem(
                row, 3, QtWidgets.QTableWidgetItem(str(data[4])))
            self.tableData.setItem(
                row, 4, QtWidgets.QTableWidgetItem(str(data[5])))
            row = row+1