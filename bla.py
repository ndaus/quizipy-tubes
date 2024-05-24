import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QIcon, QCursor
from PyQt5.QtCore import QSize, Qt
from quiz_data import quiz_data  # import data quiz dari data base

class QuizApp(QMainWindow):
    # fungsi memberi nama pada window, dan set ukuran yang fix untuk window
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QuiziPy")
        self.setFixedWidth(1920)
        self.setFixedHeight(1200)

        # untuk membuat background label
        self.background_label = QLabel(self)
        self.background_label.setGeometry(0, 0, 1920, 1200)

        # fungsi untuk mengubah background window menjadi gambar milik kita
        self.background_label.setPixmap(QPixmap("bgs.png"))

        # fungsi untuk positioning di tengah
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # memanggil fungsi layouting secara vertikal grid
        self.layout = QVBoxLayout()
        # memanggil fungsi layouting secara horizontal grid
        button_layout = QHBoxLayout()

        # fungsi untuk melayouting teks pertanyaan
        self.qs_label = QLabel("Question goes here")
        self.qs_label.setAlignment(Qt.AlignCenter)  # membuat posisi pertanyaan menjadi di tengah
        self.qs_label.setStyleSheet(
            "background-color: rgba(0, 198, 186, 0.5); color: white; font-size: 35px; border: 3px solid #00C6BA; border-radius: 25px; padding: 100px;")  # Set font color and border
        self.layout.addWidget(self.qs_label)

        self.choice_btns = []
        for i in range(4):
            button = QPushButton()
            button.setIconSize(QSize(50, 50))  # Ubah ukuran ikon menjadi 50x50 px
            button.setMinimumSize(300, 300)  # Set ukuran minimum tombol
            button.setMaximumSize(300, 300)  # Set ukuran maksimum tombol
            button.clicked.connect(lambda _, i=i: self.check_answer(i))
            button.setStyleSheet("padding: 0px;")  # Atur padding tombol menjadi 0px
            button_layout.addWidget(button)  # Tambahkan tombol ke dalam layout horizontal
            self.choice_btns.append(button)

            # Tambahkan layout horizontal tombol ke dalam layout utama
            self.layout.addLayout(button_layout)

            # Set alignment vertikal menjadi tengah
            self.layout.setAlignment(Qt.AlignVCenter)

        # Membuat border score
        self.score_border = QWidget()
        self.score_border.setStyleSheet("border: 3px solid #00C6BA; border-radius: 25px; padding: 10px;font-size: 75px;")
        self.score_layout = QVBoxLayout(self.score_border)
        self.score_layout.setContentsMargins(20, 20, 20, 20)
        self.layout.addWidget(self.score_border)

        # menambahkan score label ke score border
        self.score = 0
        self.score_label = QLabel("Score: {}/{}".format(self.score, len(quiz_data)))
        self.score_label.setAlignment(Qt.AlignCenter)
        self.score_label.setStyleSheet("color: white;")
        self.score_layout.addWidget(self.score_label)

        # Menambahkan feedback label ke score border
        self.feedback_label = QLabel()
        self.feedback_label.setAlignment(Qt.AlignCenter)
        self.feedback_label.setStyleSheet("color: white;")
        self.score_layout.addWidget(self.feedback_label)

        self.next_btn = QPushButton("Next")
        self.next_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self.next_btn.setStyleSheet(
            '''
            QPushButton {
                background-color: rgba(0, 198, 186, 0.5);
                border: 5px solid #00C6BA;
                border-radius: 25px;
                font-size: 35px;
                color: white;
                padding: 50px 0;
            }
            QPushButton:hover {
                background-color: #00C6BA;
            }
            '''
        )
        self.next_btn.clicked.connect(self.next_question)
        self.next_btn.setEnabled(False)
        self.layout.addWidget(self.next_btn)

        self.current_question = 0
        self.show_question()

        self.central_widget.setLayout(self.layout)

    def show_question(self):
        question = quiz_data[self.current_question]
        self.qs_label.setText(question["question"])

        choices = question["choices"]
        for i in range(4):
            button = self.choice_btns[i]
            button.setIconSize(QSize(200, 200))  # Atur ukuran ikon tombol
            button.setIcon(QIcon(QPixmap(choices[i])))
            button.setEnabled(True)

        self.feedback_label.clear()
        self.next_btn.setEnabled(False)

    def check_answer(self, choice):
        question = quiz_data[self.current_question] # mengambil pertanyaan dari database
        selected_choice = quiz_data[self.current_question]["choices"][choice]

        #  Memeriksa apakah pilihan yang dipilih oleh pengguna sesuai dengan jawaban yang benar
        if selected_choice == question["answer"]:
            self.score += 1
            self.score_label.setText("Score: {}/{}".format(self.score, len(quiz_data)))
            self.feedback_label.setText("Horeee jawaban kamu benar!!!")
            self.feedback_label.setStyleSheet("color: #4DFF00;")
        # kondisi jika jawaban yang dipilih salah
        else:
            self.feedback_label.setText("Yahhhh jawaban kamu salah!!!")
            self.feedback_label.setStyleSheet("color: #FF001E;")

        for button in self.choice_btns: # Menggunakan perulangan for untuk menonaktifkan semua tombol pilihan jawaban
            button.setEnabled(False)
        self.next_btn.setEnabled(True) # mengaktifkan tombol next agar bisa lanjut ke soal selanjutnya

    # fungsi untuk memberi nomor pada soal saat ini sehingga jika nomor soal saat ini masih kurang dari jumlah soal di data base maka akan menampilkan soal selanjutnya, jika tidak maka akan muncul massage box yang menampilkan score
    def next_question(self):
        self.current_question += 1
        if self.current_question < len(quiz_data):
            self.show_question()
        else:
            QMessageBox.information(self, "Quiz Completed", "Quiz Completed! Final score: {}/{}".format(self.score, len(quiz_data)))
            self.close()

# Menjalankan aplikasi kuis, menampilkan antarmuka pengguna, dan mengatur event loop utama sehingga aplikasi berjalan dengan baik.
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuizApp()
    window.show()
    sys.exit(app.exec_())
