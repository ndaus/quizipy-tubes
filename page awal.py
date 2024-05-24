import sys
import os
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QWidget, QGridLayout
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5 import QtCore

# Initialisasi aplikasi GUI
app = QApplication(sys.argv)

# Buat jendela utama
window = QWidget()
window.setFixedWidth(1920)
window.setFixedHeight(1200)
window.setWindowTitle("QuiziPy")

# Buat grid layout
grid = QGridLayout()

# Buat QLabel untuk latar belakang
background_label = QLabel(window)
background_label.setPixmap(QPixmap("bg.png"))
background_label.setGeometry(0, 0, window.width(), window.height())


# Fungsi untuk memulai permainan
def start_game():
    os.system("python bla.py")  # Menggunakan os.system untuk menjalankan perintah terminal untuk membuka file bla.py
    pass

# Kamus widget yang bisa berubah secara dinamis
widgets = {"button": []}

# Buat tombol PLAY
button = QPushButton("PLAY")
button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
button.setStyleSheet(
    '''
    *{
        border: 5px solid '#00C6BA';
        border-radius: 25px;
        font-size: 35px;
        color: 'white';
        padding: 50px 0;
        margin: 100px 1200px;
        background-color: transparent;
    }
    *:hover{
        background: '#00C6BA';
    }
    '''
)
# Tambahkan fungsi callback ke tombol
button.clicked.connect(start_game)

# Tambahkan button ke dalam grid layout
grid.addWidget(button, 0, 0, alignment=QtCore.Qt.AlignCenter)

# Atur layout utama
window.setLayout(grid)

# Tampilkan jendela
window.show()
sys.exit(app.exec()) # Berhenti ketika aplikasi ditutup
