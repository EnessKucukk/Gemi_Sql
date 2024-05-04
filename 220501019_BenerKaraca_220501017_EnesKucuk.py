import sys
from PyQt5.QtWidgets import (
     QHBoxLayout, QLabel, QLineEdit,
    QTableWidget, QTableWidgetItem, QDialog, QFormLayout
)
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery


class DatabaseManager:
    def __init__(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("gemiler.db")

        if not self.db.open():
            QMessageBox.critical(
                None, "Veritabanı hatası mevcut", QMessageBox.Ok
            )

    def create_tables(self):
        query = QSqlQuery()
        query.exec_("CREATE TABLE IF NOT EXISTS gemiler ("
                    "seri_numarasi TEXT PRIMARY KEY, "
                    "ad TEXT, "
                    "agirlik INTEGER, "
                    "yapim_yili INTEGER, "
                    "tip TEXT, "
                    "kapasite INTEGER, "
                    "max_agirlik INTEGER)")

        query.exec_("CREATE TABLE IF NOT EXISTS seferler ("
                    "sefer_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                    "yola_cikis_tarihi TEXT, "
                    "donus_tarihi TEXT, "
                    "yola_cikis_limani TEXT)")

        query.exec_("CREATE TABLE IF NOT EXISTS limanlar ("
                    "liman_adi TEXT PRIMARY KEY, "
                    "ulke TEXT, "
                    "nufus INTEGER, "
                    "pasaport_gerekli_mi TEXT, "
                    "demirleme_ucreti INTEGER)")

        query.exec_("CREATE TABLE IF NOT EXISTS kaptanlar ("
                    "kaptan_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                    "ad TEXT, "
                    "soyad TEXT, "
                    "adres TEXT, "
                    "vatandaslik TEXT, "
                    "dogum_tarihi TEXT, "
                    "ise_giris_tarihi TEXT)")

        query.exec_("CREATE TABLE IF NOT EXISTS murettebat ("
                    "murettebat_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                    "ad TEXT, "
                    "soyad TEXT, "
                    "adres TEXT, "
                    "vatandaslik TEXT, "
                    "dogum_tarihi TEXT, "
                    "ise_giris_tarihi TEXT)")

class AnaPencere(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Gezgin Gemi Şirketi Ödevi')
        self.setGeometry(100, 100, 1280, 720)

        layout = QVBoxLayout()


        gemiler_seferler_layout = QHBoxLayout()


        lbl_petrol_gemileri = QLabel('Petrol Gemileri')
        gemiler_seferler_layout.addWidget(lbl_petrol_gemileri)
        petrol_gemileri_ekrani = GemilerEkrani("petrol")
        gemiler_seferler_layout.addWidget(petrol_gemileri_ekrani)


        lbl_yolcu_gemileri = QLabel('Yolcu Gemileri')
        gemiler_seferler_layout.addWidget(lbl_yolcu_gemileri)
        yolcu_gemileri_ekrani = GemilerEkrani("yolcu")
        gemiler_seferler_layout.addWidget(yolcu_gemileri_ekrani)


        lbl_konteyner_gemileri = QLabel('Konteyner Gemileri')
        gemiler_seferler_layout.addWidget(lbl_konteyner_gemileri)
        konteyner_gemileri_ekrani = GemilerEkrani("konteyner")
        gemiler_seferler_layout.addWidget(konteyner_gemileri_ekrani)

        layout.addLayout(gemiler_seferler_layout)


        seferler_murettebat_layout = QHBoxLayout()


        lbl_seferler = QLabel('Seferler')
        seferler_murettebat_layout.addWidget(lbl_seferler)
        seferler_ekrani = SeferlerEkrani()
        seferler_murettebat_layout.addWidget(seferler_ekrani)


        btn_ekle_sefer = QPushButton('Ekle')
        btn_ekle_sefer.clicked.connect(seferler_ekrani.sefer_ekle_dialog_ac)
        seferler_murettebat_layout.addWidget(btn_ekle_sefer)

        layout.addLayout(seferler_murettebat_layout)


        limanlar_kaptanlar_layout = QHBoxLayout()


        lbl_limanlar = QLabel('Limanlar')
        limanlar_kaptanlar_layout.addWidget(lbl_limanlar)
        limanlar_ekrani = LimanlarEkrani()
        limanlar_kaptanlar_layout.addWidget(limanlar_ekrani)


        btn_ekle_liman = QPushButton('Ekle')
        btn_ekle_liman.clicked.connect(limanlar_ekrani.liman_ekle_dialog_ac)
        limanlar_kaptanlar_layout.addWidget(btn_ekle_liman)

        layout.addLayout(limanlar_kaptanlar_layout)


        lbl_kaptanlar = QLabel('Kaptanlar')
        limanlar_kaptanlar_layout.addWidget(lbl_kaptanlar)
        kaptanlar_ekrani = KaptanlarEkrani()
        limanlar_kaptanlar_layout.addWidget(kaptanlar_ekrani)


        btn_ekle_kaptan = QPushButton('Ekle')
        btn_ekle_kaptan.clicked.connect(kaptanlar_ekrani.kaptan_ekle_dialog_ac)
        limanlar_kaptanlar_layout.addWidget(btn_ekle_kaptan)

        layout.addLayout(limanlar_kaptanlar_layout)


        lbl_murettebat = QLabel('Mürettebat')
        layout.addWidget(lbl_murettebat)
        murettebat_ekrani = MurettebatEkrani()
        layout.addWidget(murettebat_ekrani)

        btn_ekle_murettebat = QPushButton('Ekle')
        btn_ekle_murettebat.clicked.connect(murettebat_ekrani.murettebat_ekle_dialog_ac)
        layout.addWidget(btn_ekle_murettebat)

        self.setLayout(layout)


class GemilerEkrani(QWidget):
    def __init__(self, gemi_turu):
        super().__init__()
        self.gemi_turu = gemi_turu
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.table_gemiler = QTableWidget()
        self.table_gemiler.setColumnCount(7)
        self.table_gemiler.setHorizontalHeaderLabels(
            ['Seri Numarası', 'Ad', 'Ağırlık', 'Yapım Yılı', 'Tip', 'Kapasite', 'Maksimum Ağırlık'])
        layout.addWidget(self.table_gemiler)


        btn_ekle = QPushButton('Ekle')
        btn_ekle.clicked.connect(self.gemi_ekle_dialog_ac)
        layout.addWidget(btn_ekle)


        btn_sil = QPushButton('Sil')
        btn_sil.clicked.connect(self.gemi_sil)
        layout.addWidget(btn_sil)

        self.setLayout(layout)

    def gemi_ekle_dialog_ac(self):
        dialog = QDialog()
        dialog.setWindowTitle('Yeni Gemi Ekle')

        layout = QFormLayout()

        self.txt_seri_numarasi = QLineEdit()
        self.txt_ad = QLineEdit()
        self.txt_agirlik = QLineEdit()
        self.txt_yapim_yili = QLineEdit()
        self.txt_tip = QLineEdit()
        self.txt_kapasite = QLineEdit()
        self.txt_max_agirlik = QLineEdit()

        layout.addRow('Seri Numarası:', self.txt_seri_numarasi)
        layout.addRow('Ad:', self.txt_ad)
        layout.addRow('Ağırlık:', self.txt_agirlik)
        layout.addRow('Yapım Yılı:', self.txt_yapim_yili)
        layout.addRow('Tip:', self.txt_tip)
        layout.addRow('Kapasite:', self.txt_kapasite)
        layout.addRow('Maksimum Ağırlık:', self.txt_max_agirlik)

        btn_kaydet = QPushButton('Kaydet')
        btn_kaydet.clicked.connect(self.yeni_gemi_kaydet)

        layout.addWidget(btn_kaydet)

        dialog.setLayout(layout)
        dialog.exec()

    def yeni_gemi_kaydet(self):
        seri_numarasi = self.txt_seri_numarasi.text()
        ad = self.txt_ad.text()
        agirlik = self.txt_agirlik.text()
        yapim_yili = self.txt_yapim_yili.text()
        tip = self.txt_tip.text()
        kapasite = self.txt_kapasite.text()
        max_agirlik = self.txt_max_agirlik.text()


        row_count = self.table_gemiler.rowCount()
        self.table_gemiler.insertRow(row_count)
        self.table_gemiler.setItem(row_count, 0, QTableWidgetItem(seri_numarasi))
        self.table_gemiler.setItem(row_count, 1, QTableWidgetItem(ad))
        self.table_gemiler.setItem(row_count, 2, QTableWidgetItem(agirlik))
        self.table_gemiler.setItem(row_count, 3, QTableWidgetItem(yapim_yili))
        self.table_gemiler.setItem(row_count, 4, QTableWidgetItem(tip))
        self.table_gemiler.setItem(row_count, 5, QTableWidgetItem(kapasite))
        self.table_gemiler.setItem(row_count, 6, QTableWidgetItem(max_agirlik))

    def gemi_sil(self):
        selected_row = self.table_gemiler.currentRow()
        if selected_row != -1:
            self.table_gemiler.removeRow(selected_row)
        else:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen bir satır seçin.')


class SeferlerEkrani(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()


        self.table_seferler = QTableWidget()
        self.table_seferler.setColumnCount(4)
        self.table_seferler.setHorizontalHeaderLabels(['ID', 'Yola Çıkış Tarihi', 'Dönüş Tarihi', 'Yola Çıkış Limanı'])
        layout.addWidget(self.table_seferler)

        btn_ekle = QPushButton('Ekle')
        btn_ekle.clicked.connect(self.sefer_ekle_dialog_ac)
        layout.addWidget(btn_ekle)

        btn_sil = QPushButton('Sil')
        btn_sil.clicked.connect(self.sefer_sil)
        layout.addWidget(btn_sil)

        self.setLayout(layout)

    def sefer_ekle_dialog_ac(self):
        dialog = QDialog()
        dialog.setWindowTitle('Yeni Sefer Ekle')

        layout = QFormLayout()

        self.txt_sefer_id = QLineEdit()
        self.txt_yola_cikis_tarihi = QLineEdit()
        self.txt_donus_tarihi = QLineEdit()
        self.txt_yola_cikis_limanı = QLineEdit()

        layout.addRow('ID:', self.txt_sefer_id)
        layout.addRow('Yola Çıkış Tarihi:', self.txt_yola_cikis_tarihi)
        layout.addRow('Dönüş Tarihi:', self.txt_donus_tarihi)
        layout.addRow('Yola Çıkış Limanı:', self.txt_yola_cikis_limanı)

        btn_kaydet = QPushButton('Kaydet')
        btn_kaydet.clicked.connect(self.yeni_sefer_kaydet)

        layout.addWidget(btn_kaydet)

        dialog.setLayout(layout)
        dialog.exec()

    def yeni_sefer_kaydet(self):
        sefer_id = self.txt_sefer_id.text()
        yola_cikis_tarihi = self.txt_yola_cikis_tarihi.text()
        donus_tarihi = self.txt_donus_tarihi.text()
        yola_cikis_limanı = self.txt_yola_cikis_limanı.text()

        row_count = self.table_seferler.rowCount()
        self.table_seferler.insertRow(row_count)
        self.table_seferler.setItem(row_count, 0, QTableWidgetItem(sefer_id))
        self.table_seferler.setItem(row_count, 1, QTableWidgetItem(yola_cikis_tarihi))
        self.table_seferler.setItem(row_count, 2, QTableWidgetItem(donus_tarihi))
        self.table_seferler.setItem(row_count, 3, QTableWidgetItem(yola_cikis_limanı))

    def sefer_sil(self):
        selected_row = self.table_seferler.currentRow()
        if selected_row != -1:
            self.table_seferler.removeRow(selected_row)
        else:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen bir satır seçin.')


class LimanlarEkrani(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.table_limanlar = QTableWidget()
        self.table_limanlar.setColumnCount(5)
        self.table_limanlar.setHorizontalHeaderLabels(
            ['Liman Adı', 'Ülke', 'Nüfus', 'Pasaport Gerekli mi?', 'Demirleme Ücreti'])
        layout.addWidget(self.table_limanlar)

        btn_ekle = QPushButton('Ekle')
        btn_ekle.clicked.connect(self.liman_ekle_dialog_ac)
        layout.addWidget(btn_ekle)

        btn_sil = QPushButton('Sil')
        btn_sil.clicked.connect(self.liman_sil)
        layout.addWidget(btn_sil)

        self.setLayout(layout)

    def liman_ekle_dialog_ac(self):
        dialog = QDialog()
        dialog.setWindowTitle('Yeni Liman Ekle')

        layout = QFormLayout()

        self.txt_liman_adi = QLineEdit()
        self.txt_ulke = QLineEdit()
        self.txt_nufus = QLineEdit()
        self.txt_pasaport_gerekli_mi = QLineEdit()
        self.txt_demirleme_ucreti = QLineEdit()

        layout.addRow('Liman Adı:', self.txt_liman_adi)
        layout.addRow('Ülke:', self.txt_ulke)
        layout.addRow('Nüfus:', self.txt_nufus)
        layout.addRow('Pasaport Gerekli mi:', self.txt_pasaport_gerekli_mi)
        layout.addRow('Demirleme Ücreti:', self.txt_demirleme_ucreti)

        btn_kaydet = QPushButton('Kaydet')
        btn_kaydet.clicked.connect(self.yeni_liman_kaydet)

        layout.addWidget(btn_kaydet)

        dialog.setLayout(layout)
        dialog.exec()

    def yeni_liman_kaydet(self):
        liman_adi = self.txt_liman_adi.text()
        ulke = self.txt_ulke.text()
        nufus = self.txt_nufus.text()
        pasaport_gerekli_mi = self.txt_pasaport_gerekli_mi.text()
        demirleme_ucreti = self.txt_demirleme_ucreti.text()

        row_count = self.table_limanlar.rowCount()
        self.table_limanlar.insertRow(row_count)
        self.table_limanlar.setItem(row_count, 0, QTableWidgetItem(liman_adi))
        self.table_limanlar.setItem(row_count, 1, QTableWidgetItem(ulke))
        self.table_limanlar.setItem(row_count, 2, QTableWidgetItem(nufus))
        self.table_limanlar.setItem(row_count, 3, QTableWidgetItem(pasaport_gerekli_mi))
        self.table_limanlar.setItem(row_count, 4, QTableWidgetItem(demirleme_ucreti))

    def liman_sil(self):
        selected_row = self.table_limanlar.currentRow()
        if selected_row != -1:
            self.table_limanlar.removeRow(selected_row)
        else:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen bir satır seçin.')


class KaptanlarEkrani(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.table_kaptanlar = QTableWidget()
        self.table_kaptanlar.setColumnCount(7)
        self.table_kaptanlar.setHorizontalHeaderLabels(
            ['ID', 'Ad', 'Soyad', 'Adres', 'Vatandaşlık', 'Doğum Tarihi', 'İşe Giriş Tarihi'])
        layout.addWidget(self.table_kaptanlar)

        btn_ekle = QPushButton('Ekle')
        btn_ekle.clicked.connect(self.kaptan_ekle_dialog_ac)
        layout.addWidget(btn_ekle)

        btn_sil = QPushButton('Sil')
        btn_sil.clicked.connect(self.kaptan_sil)
        layout.addWidget(btn_sil)

        self.setLayout(layout)

    def kaptan_ekle_dialog_ac(self):
        dialog = QDialog()
        dialog.setWindowTitle('Yeni Kaptan Ekle')

        layout = QFormLayout()

        self.txt_kaptan_id = QLineEdit()
        self.txt_ad = QLineEdit()
        self.txt_soyad = QLineEdit()
        self.txt_adres = QLineEdit()
        self.txt_vatandaslik = QLineEdit()
        self.txt_dogum_tarihi = QLineEdit()
        self.txt_ise_giris_tarihi = QLineEdit()

        layout.addRow('ID:', self.txt_kaptan_id)
        layout.addRow('Ad:', self.txt_ad)
        layout.addRow('Soyad:', self.txt_soyad)
        layout.addRow('Adres:', self.txt_adres)
        layout.addRow('Vatandaşlık:', self.txt_vatandaslik)
        layout.addRow('Doğum Tarihi:', self.txt_dogum_tarihi)
        layout.addRow('İşe Giriş Tarihi:', self.txt_ise_giris_tarihi)

        btn_kaydet = QPushButton('Kaydet')
        btn_kaydet.clicked.connect(self.yeni_kaptan_kaydet)

        layout.addWidget(btn_kaydet)

        dialog.setLayout(layout)
        dialog.exec()

    def yeni_kaptan_kaydet(self):
        kaptan_id = self.txt_kaptan_id.text()
        ad = self.txt_ad.text()
        soyad = self.txt_soyad.text()
        adres = self.txt_adres.text()
        vatandaslik = self.txt_vatandaslik.text()
        dogum_tarihi = self.txt_dogum_tarihi.text()
        ise_giris_tarihi = self.txt_ise_giris_tarihi.text()

        row_count = self.table_kaptanlar.rowCount()
        self.table_kaptanlar.insertRow(row_count)
        self.table_kaptanlar.setItem(row_count, 0, QTableWidgetItem(kaptan_id))
        self.table_kaptanlar.setItem(row_count, 1, QTableWidgetItem(ad))
        self.table_kaptanlar.setItem(row_count, 2, QTableWidgetItem(soyad))
        self.table_kaptanlar.setItem(row_count, 3, QTableWidgetItem(adres))
        self.table_kaptanlar.setItem(row_count, 4, QTableWidgetItem(vatandaslik))
        self.table_kaptanlar.setItem(row_count, 5, QTableWidgetItem(dogum_tarihi))
        self.table_kaptanlar.setItem(row_count, 6, QTableWidgetItem(ise_giris_tarihi))

    def kaptan_sil(self):
        selected_row = self.table_kaptanlar.currentRow()
        if selected_row != -1:
            self.table_kaptanlar.removeRow(selected_row)
        else:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen bir satır seçin.')


class MurettebatEkrani(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.table_murettebat = QTableWidget()
        self.table_murettebat.setColumnCount(7)
        self.table_murettebat.setHorizontalHeaderLabels(
            ['ID', 'Ad', 'Soyad', 'Adres','Vatandaşlık','Doğum Tarihi','İşe giriş tarihi'])
        layout.addWidget(self.table_murettebat)

        btn_ekle = QPushButton('Ekle')
        btn_ekle.clicked.connect(self.murettebat_ekle_dialog_ac)
        layout.addWidget(btn_ekle)

        btn_sil = QPushButton('Sil')
        btn_sil.clicked.connect(self.murettebat_sil)
        layout.addWidget(btn_sil)

        self.setLayout(layout)

    def murettebat_ekle_dialog_ac(self):
        dialog = QDialog()
        dialog.setWindowTitle('Yeni Mürettebat Ekle')

        layout = QFormLayout()

        self.txt_murettebat_id = QLineEdit()
        self.txt_ad = QLineEdit()
        self.txt_soyad = QLineEdit()
        self.txt_adres = QLineEdit()
        self.txt_vatandaslik = QLineEdit()
        self.txt_dogum_tarihi = QLineEdit()
        self.txt_ise_giris_tarihi = QLineEdit()

        layout.addRow('ID:', self.txt_murettebat_id)
        layout.addRow('Ad:', self.txt_ad)
        layout.addRow('Soyad:', self.txt_soyad)
        layout.addRow('Vatandaşlık:', self.txt_vatandaslik)
        layout.addRow('Adres:', self.txt_adres)
        layout.addRow('Doğum Tarihi:', self.txt_dogum_tarihi)
        layout.addRow('İşe Giriş Tarihi:', self.txt_ise_giris_tarihi)

        btn_kaydet = QPushButton('Kaydet')
        btn_kaydet.clicked.connect(self.yeni_murettebat_kaydet)

        layout.addWidget(btn_kaydet)

        dialog.setLayout(layout)
        dialog.exec()

    def yeni_murettebat_kaydet(self):
        murettebat_id = self.txt_murettebat_id.text()
        ad = self.txt_ad.text()
        soyad = self.txt_soyad.text()
        dogum_tarihi = self.txt_dogum_tarihi.text()
        ise_giris_tarihi = self.txt_ise_giris_tarihi.text()
        vatandaslik = self.txt_vatandaslik.text()


        row_count = self.table_murettebat.rowCount()
        self.table_murettebat.insertRow(row_count)
        self.table_murettebat.setItem(row_count, 0, QTableWidgetItem(murettebat_id))
        self.table_murettebat.setItem(row_count, 1, QTableWidgetItem(ad))
        self.table_murettebat.setItem(row_count, 2, QTableWidgetItem(soyad))
        self.table_murettebat.setItem(row_count, 4, QTableWidgetItem(vatandaslik))
        self.table_murettebat.setItem(row_count, 5, QTableWidgetItem(dogum_tarihi))
        self.table_murettebat.setItem(row_count, 6, QTableWidgetItem(ise_giris_tarihi))

    def murettebat_sil(self):
        selected_row = self.table_murettebat.currentRow()
        if selected_row != -1:
            self.table_murettebat.removeRow(selected_row)
        else:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen bir satır seçin.')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ana_pencere = AnaPencere()
    ana_pencere.show()
    sys.exit(app.exec())