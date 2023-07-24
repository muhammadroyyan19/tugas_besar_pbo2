import sys
from PyQt5 import QtWidgets, uic
from admin.dosen import *
from admin.prodi import *
from admin.mahasiswa import *
from admin.sidang import *
from admin.v_jadwal_sidang import *

class Dashboard(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("admin/dashboard.ui", self)
        self.actDosen.triggered.connect(self.menuDosen)
        self.actMahasiswa.triggered.connect(self.menuMahasiswa)
        self.actFakultas.triggered.connect(self.menuProdi)
        self.actSidang.triggered.connect(self.menuSidang)
        self.actJadwalSidang.triggered.connect(self.viewSidang)
        self.actLogout.triggered.connect(self.logout)
        pass

    def menuDosen(self):
        self.wdow = Dosen()
        self.wdow.show()

    def menuMahasiswa(self):
        self.wdow = Mahasiswa()
        self.wdow.show()

    def menuProdi(self):
        self.wdow = Prodi()
        self.wdow.show()

    def menuSidang(self):
        self.wdow = Sidang()
        self.wdow.show()

    def viewSidang(self):
        self.wdow = JadwalSidang()
        self.wdow.show()

    def logout(self):
        sys.exit()