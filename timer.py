import sys
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget, QApplication, QPushButton
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtMultimedia import QSound
from PyQt5.QtGui import QFont, QFontDatabase

class timer(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(800, 500, 600, 500)
        self.display_angka = QLabel("00:00:00", self)
        self.angka1 = QPushButton("1", self)
        self.angka2 = QPushButton("2", self)
        self.angka3 = QPushButton("3", self)
        self.angka4 = QPushButton("4", self)
        self.angka5 = QPushButton("5", self)
        self.angka6 = QPushButton("6", self)
        self.angka7 = QPushButton("7", self)
        self.angka8 = QPushButton("8", self)
        self.angka9 = QPushButton("9", self)
        self.angka0 = QPushButton("0", self)
        self.mulai = QPushButton("▶", self)
        self.hapus = QPushButton("←", self)

        self.pause_btn = QPushButton("⏸", self)
        self.stop_btn = QPushButton("■", self)
        self.reset_btn = QPushButton("⟳", self)
        self.resume_btn = QPushButton("▶", self)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        self.time_input = ""
        self.time_left = 0
        self.original_time_left = 0
        self.timer_running = False
        self.paused = False

        self.alarm_playing = False
        self.alarm = QSound("soundeffect.wav")

        self.ui()

    def ui(self):
        self.setWindowTitle("timer")
        v = QVBoxLayout()

        self.display_angka.setAlignment(Qt.AlignCenter)
        self.display_angka.setStyleSheet("font-size: 50px;"
                                         "font-family: Arial;"
                                         "color: white;"
                                         "font-weight: bold;"
                                         "border: 2px solid white;")
        v.addWidget(self.display_angka)

        for row in ([self.angka1, self.angka2, self.angka3],
                    [self.angka4, self.angka5, self.angka6],
                    [self.angka7, self.angka8, self.angka9]):
            h = QHBoxLayout()
            for btn in row:
                h.addWidget(btn)
                btn.clicked.connect(self.input_digit)
            v.addLayout(h)

        row4 = QHBoxLayout()
        self.angka0.clicked.connect(self.input_digit)
        row4.addWidget(self.hapus)
        row4.addWidget(self.angka0)
        row4.addWidget(self.mulai)
        v.addLayout(row4)

        row5 = QHBoxLayout()
        row5.addWidget(self.pause_btn)
        row5.addWidget(self.resume_btn)
        row5.addWidget(self.stop_btn)
        row5.addWidget(self.reset_btn)
        v.addLayout(row5)

        self.setLayout(v)
        
        self.setStyleSheet("""
            QWidget {
                background-color: black;
            }
            
            QPushButton {
                font-size: 40px;
                padding: 15px;
                color: white;
                background-color: lime;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: lightgreen;
            }
            QPushButton:pressed {
                background-color: green;
            }             
        """)
        self.display_angka.setStyleSheet("font-size: 80px;"
                                         "color: white;"
                                         "border: 2px solid white;")

        font = QFontDatabase.addApplicationFont("DS-DIGIT.TTF")
        font_family = QFontDatabase.applicationFontFamilies(font)[0]
        my_font = QFont(font_family)
        self.display_angka.setFont(my_font)
        self.pause_btn.setFont(my_font)
        self.stop_btn.setFont(my_font)
        self.reset_btn.setFont(my_font)
        self.resume_btn.setFont(my_font)
        self.angka1.setFont(my_font)
        self.angka2.setFont(my_font)
        self.angka3.setFont(my_font)
        self.angka4.setFont(my_font)
        self.angka5.setFont(my_font)
        self.angka6.setFont(my_font)
        self.angka7.setFont(my_font)
        self.angka8.setFont(my_font)
        self.angka9.setFont(my_font)
        self.angka0.setFont(my_font)
        self.hapus.setFont(my_font)
        self.mulai.setFont(my_font)
       

        self.hapus.clicked.connect(self.delete_digit)
        self.mulai.clicked.connect(self.start_timer)
        self.pause_btn.clicked.connect(self.pause_timer)
        self.resume_btn.clicked.connect(self.resume_timer)
        self.stop_btn.clicked.connect(self.stop_timer)
        self.reset_btn.clicked.connect(self.reset_timer)

        self.toggle_timer_controls(False)

    def input_digit(self):
        if self.timer_running:
            return
        if len(self.time_input) >= 6:
            return
        self.time_input += self.sender().text()
        self.update_display()

    def delete_digit(self):
        if self.timer_running:
            return
        self.time_input = self.time_input[:-1]
        self.update_display()

    def update_display(self):
        padded = self.time_input.rjust(6, '0')
        h, m, s = padded[:2], padded[2:4], padded[4:]
        self.display_angka.setText(f"{h}:{m}:{s}")

    def start_timer(self):
        if not self.time_input:
            return
        padded = self.time_input.rjust(6, '0')
        h, m, s = int(padded[:2]), int(padded[2:4]), int(padded[4:])
        self.time_left = h * 3600 + m * 60 + s
        self.original_time_left = self.time_left
        if self.time_left == 0:
            return

        self.timer.start(1000)
        self.timer_running = True
        self.paused = False
        self.update_timer_display()
        self.toggle_inputs(False)
        self.toggle_timer_controls(True)

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.update_timer_display()
        else:
            self.timer.stop()
            self.play_alarm()
            self.timer_running = False
            self.display_angka.setText("00:00:00")
            self.toggle_inputs(False)

            self.pause_btn.hide()
            self.resume_btn.hide()
            self.reset_btn.hide()
            self.stop_btn.setVisible(True)
            self.stop_btn.setEnabled(True)

    def update_timer_display(self):
        h = self.time_left // 3600
        m = (self.time_left % 3600) // 60
        s = self.time_left % 60
        self.display_angka.setText(f"{h:02}:{m:02}:{s:02}")

    def pause_timer(self):
        self.timer.stop()
        self.timer_running = False
        self.paused = True
        self.pause_btn.hide()
        self.resume_btn.setVisible(True)
        self.resume_btn.setEnabled(True)

    def resume_timer(self):
        self.timer.start(1000)
        self.timer_running = True
        self.paused = False
        self.pause_btn.setVisible(True)
        self.resume_btn.setVisible(False)

    def reset_timer(self):
        self.time_left = self.original_time_left
        self.update_timer_display()
        if not self.timer_running:
            self.timer.start(1000)
            self.timer_running = True
        self.resume_btn.hide()
        self.pause_btn.show()

    def stop_timer(self):
        self.timer.stop()
        self.timer_running = False
        self.paused = False
        self.time_input = ""
        self.time_left = 0
        self.original_time_left = 0
        self.display_angka.setText("00:00:00")
        self.toggle_inputs(True)
        self.toggle_timer_controls(False)

        if self.alarm_playing:
            self.alarm.stop()
            self.alarm_playing = False

    def toggle_inputs(self, enable):
        for btn in [self.angka0, self.angka1, self.angka2, self.angka3, self.angka4,
                    self.angka5, self.angka6, self.angka7, self.angka8, self.angka9,
                    self.angka0,self.hapus, self.mulai]:
            btn.setEnabled(enable)
            btn.setVisible(enable)

    def toggle_timer_controls(self, show):
        self.pause_btn.setVisible(show)
        self.pause_btn.setEnabled(show)
        self.stop_btn.setVisible(show)
        self.stop_btn.setEnabled(show)
        self.reset_btn.setVisible(show)
        self.reset_btn.setEnabled(show)
        self.resume_btn.hide()
        self.resume_btn.setEnabled(True)

    def play_alarm(self):
        if not self.alarm_playing:
            self.alarm.setLoops(QSound.Infinite)
            self.alarm.play()
            self.alarm_playing = True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = timer()
    window.show()
    sys.exit(app.exec_())
