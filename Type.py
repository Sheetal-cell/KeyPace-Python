import sys
import random
import time
import json
import os
from datetime import datetime
from PyQt6.QtWidgets import QScrollArea
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QProgressBar, QStackedWidget, QTableWidget,
    QTableWidgetItem, QMessageBox, QHBoxLayout, QSpacerItem,
    QSizePolicy, QDialog, QInputDialog
)
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QFont, QColor, QPalette, QAction


PASSAGES = [
    "The quick brown fox jumps over the lazy dog.",
    "Python is a versatile programming language.",
    "Practice makes perfect when it comes to typing.",
    "Stay focused and keep improving your pace.",
    "Typing fast is a useful skill for everyone.",
    "The sun sets in the west and rises in the east.",
    "Knowledge is power and enthusiasm pulls the switch.",
    "Never stop exploring new opportunities and ideas.",
    "Challenges make life interesting and rewarding.",
    "Keep calm and code on with Python.",
    "Good habits formed at youth make all the difference.",
    "Typing with speed and accuracy is a valuable asset.",
    "Work smart, stay humble, and hustle hard.",
    "Patience and practice pave the path to perfection.",
    "Every moment is a fresh beginning, make it count."
]
LEADERBOARD_FILE = "leaderboard.json"

def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    with open(LEADERBOARD_FILE, "r") as f:
        return json.load(f)

def save_leaderboard(scores):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(scores, f, indent=2)


class TypingTestApp(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("KeyPace Typing Test")
        self.resize(800, 500)
        self.setMinimumSize(600, 400)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.setStyleSheet(self.light_theme())

        self.stacked_widget = QStackedWidget()
        self.welcome_screen = WelcomeScreen(self)
        self.test_screen = TestScreen(self)
        self.result_screen = ResultScreen(self)
        self.leaderboard_screen = LeaderboardScreen(self)
        self.settings_screen = SettingsScreen(self)

        self.stacked_widget.addWidget(self.welcome_screen)
        self.stacked_widget.addWidget(self.test_screen)
        self.stacked_widget.addWidget(self.result_screen)
        self.stacked_widget.addWidget(self.leaderboard_screen)
        self.stacked_widget.addWidget(self.settings_screen)

        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

        self.current_theme = "light"

    def switch_screen(self, screen_name):
        screens = {
            "welcome": 0,
            "test": 1,
            "result": 2,
            "leaderboard": 3,
            "settings": 4
        }
        if screen_name == "leaderboard":
            self.leaderboard_screen.load_scores()
        self.stacked_widget.setCurrentIndex(screens[screen_name])

    def set_theme(self, theme):
        if theme == "dark":
            self.setStyleSheet(self.dark_theme())
            self.current_theme = "dark"
        else:
            self.setStyleSheet(self.light_theme())
            self.current_theme = "light"

    def light_theme(self):
        return """
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #a8edea, stop:1 #fed6e3);
                color: #222;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            QLabel#titleLabel {
                font-size: 36px;
                font-weight: 700;
                color: #4b0082;
            }
            QLabel#subtitleLabel {
                font-size: 18px;
                font-weight: 500;
                color: #6a1b9a;
            }
            QPushButton {
                background-color: #4b0082;
                color: white;
                border-radius: 12px;
                padding: 12px 25px;
                font-size: 16px;
                font-weight: 600;
                transition: background-color 0.3s ease;
            }
            QPushButton:hover {
                background-color: #6a1b9a;
            }
            QLineEdit {
                border: 2px solid #4b0082;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
            }
            QProgressBar {
                border: 2px solid #4b0082;
                border-radius: 10px;
                text-align: center;
                font-weight: bold;
                color: #4b0082;
            }
            QProgressBar::chunk {
                background-color: #6a1b9a;
                border-radius: 10px;
            }
            QTableWidget {
                background-color: transparent;
                border: none;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #4b0082;
                color: white;
                font-weight: 600;
                font-size: 14px;
            }
        """

    def dark_theme(self):
        return """
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #141e30, stop:1 #243b55);
                color: #eee;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            QLabel#titleLabel {
                font-size: 36px;
                font-weight: 700;
                color: #bb86fc;
            }
            QLabel#subtitleLabel {
                font-size: 18px;
                font-weight: 500;
                color: #bb86fc;
            }
            QPushButton {
                background-color: #6200ee;
                color: white;
                border-radius: 12px;
                padding: 12px 25px;
                font-size: 16px;
                font-weight: 600;
                transition: background-color 0.3s ease;
            }
            QPushButton:hover {
                background-color: #3700b3;
            }
            QLineEdit {
                border: 2px solid #bb86fc;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                background-color: #1f1b24;
                color: #eee;
            }
            QProgressBar {
                border: 2px solid #bb86fc;
                border-radius: 10px;
                text-align: center;
                font-weight: bold;
                color: #bb86fc;
            }
            QProgressBar::chunk {
                background-color: #bb86fc;
                border-radius: 10px;
            }
            QTableWidget {
                background-color: transparent;
                border: none;
                font-size: 14px;
                color: #8eed28;
                alternate-background-color: #260f38;
                gridline-color: #444;
            }
            QHeaderView::section {
                background-color: #6200ee;
                color: white;
                font-weight: 600;
                font-size: 14px;
            }
        """

class WelcomeScreen(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(50, 30, 50, 30)
        self.title = QLabel("KeyPace")
        self.title.setObjectName("titleLabel")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle = QLabel("Type Fast. Type Smart. Beat your best!")
        self.subtitle.setObjectName("subtitleLabel")
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        btn_start = QPushButton("Start Typing Test")
        btn_start.clicked.connect(lambda: self.parent.switch_screen("test"))
        btn_leaderboard = QPushButton("Leaderboard")
        btn_leaderboard.clicked.connect(lambda: self.parent.switch_screen("leaderboard"))
        btn_settings = QPushButton("Settings")
        btn_settings.clicked.connect(lambda: self.parent.switch_screen("settings"))
        btn_exit = QPushButton("Exit")
        btn_exit.clicked.connect(self.parent.close)
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.title)
        layout.addWidget(self.subtitle)
        layout.addStretch(1)  
        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(15)
        btn_layout.addWidget(btn_start)
        btn_layout.addWidget(btn_leaderboard)
        btn_layout.addWidget(btn_settings)
        btn_layout.addWidget(btn_exit)
        layout.addLayout(btn_layout)
        self.setLayout(layout)


class TestScreen(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.passage = ""
        self.start_time = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.elapsed = 0

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(15)
        self.instruction = QLabel("Type the following passage:")
        self.instruction.setFont(QFont("Segoe UI", 14))
        self.instruction.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.passage_label = QLabel("")
        self.passage_label.setWordWrap(True)
        self.passage_label.setFont(QFont("Segoe UI", 16))
        self.passage_label.setStyleSheet("color: #4b0082;")
        self.passage_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(25)
        self.progress_bar.setValue(0)
        self.input_field = QLineEdit()
        self.input_field.setMinimumWidth(300)
        self.input_field.setFont(QFont("Segoe UI", 14))
        self.input_field.textChanged.connect(self.on_text_changed)
        stats_layout = QHBoxLayout()
        self.wpm_label = QLabel("WPM: 0")
        self.accuracy_label = QLabel("Accuracy: 0%")
        self.wpm_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.accuracy_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        stats_layout.addWidget(self.wpm_label)
        stats_layout.addStretch()
        stats_layout.addWidget(self.accuracy_label)
        btn_layout = QHBoxLayout()
        btn_finish = QPushButton("Finish")
        btn_finish.clicked.connect(self.finish_test)
        btn_back = QPushButton("Back")
        btn_back.clicked.connect(lambda: self.parent.switch_screen("welcome"))
        btn_layout.addWidget(btn_back)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_finish)
        layout.addWidget(self.instruction)
        layout.addWidget(self.passage_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.input_field)
        layout.addLayout(stats_layout)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def start_test(self):

        self.passage = random.choice(PASSAGES)
        self.passage_label.setText(self.passage)
        self.input_field.clear()
        self.progress_bar.setValue(0)
        self.wpm_label.setText("WPM: 0")
        self.accuracy_label.setText("Accuracy: 0%")
        self.start_time = None
        self.elapsed = 0
        self.timer.stop()
        self.input_field.setEnabled(True)
        self.input_field.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        QTimer.singleShot(100, self.input_field.setFocus)
        self.input_field.setFocus()

    def on_text_changed(self):
        if self.start_time is None:
            self.start_time = time.time()
            self.timer.start(1000)

        typed = self.input_field.text()
        total_len = len(self.passage)
        correct_chars = sum(1 for i, c in enumerate(typed) if i < total_len and c == self.passage[i])

        progress = min(len(typed) / total_len * 100, 100)
        self.progress_bar.setValue(int(progress))

        self.elapsed = max(time.time() - self.start_time, 1)
        words_typed = len(typed.split())
        wpm = (words_typed / self.elapsed) * 60
        accuracy = (correct_chars / total_len) * 100 if total_len else 0

        self.wpm_label.setText(f"WPM: {wpm:.2f}")
        self.accuracy_label.setText(f"Accuracy: {accuracy:.2f}%")

        if typed == self.passage:
            self.finish_test()

    def update_stats(self):

        typed = self.input_field.text()
        total_len = len(self.passage)
        correct_chars = sum(1 for i, c in enumerate(typed) if i < total_len and c == self.passage[i])

        progress = min(len(typed) / total_len * 100, 100)
        self.progress_bar.setValue(int(progress))

        self.elapsed = max(time.time() - self.start_time, 1)
        words_typed = len(typed.split())
        wpm = (words_typed / self.elapsed) * 60
        accuracy = (correct_chars / total_len) * 100 if total_len else 0

        self.wpm_label.setText(f"WPM: {wpm:.2f}")
        self.accuracy_label.setText(f"Accuracy: {accuracy:.2f}%")

    def finish_test(self):

        self.timer.stop()
        self.input_field.setEnabled(False)
        typed = self.input_field.text()
        total_len = len(self.passage)
        correct_chars = sum(1 for i, c in enumerate(typed) if i < total_len and c == self.passage[i])
        elapsed = max(time.time() - self.start_time, 1)
        words_typed = len(typed.split())
        wpm = (words_typed / elapsed) * 60
        accuracy = (correct_chars / total_len) * 100 if total_len else 0

        self.parent.result_screen.set_results(wpm, accuracy, self.passage)
        self.parent.switch_screen("result")

    def showEvent(self, event):
        super().showEvent(event)
        self.start_test()

class ResultScreen(QWidget):

    def __init__(self, parent):

        super().__init__()
        self.parent = parent
        self.wpm = 0
        self.accuracy = 0
        self.passage = ""
        self.init_ui()

    def init_ui(self):

        layout = QVBoxLayout()
        layout.setContentsMargins(50, 40, 50, 40)
        layout.setSpacing(20)

        self.result_label = QLabel("")
        self.result_label.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_save = QPushButton("Save to Leaderboard")
        btn_save.clicked.connect(self.save_score)

        btn_retry = QPushButton("Try Again")
        btn_retry.clicked.connect(lambda: self.parent.switch_screen("test"))

        btn_leaderboard = QPushButton("Leaderboard")
        btn_leaderboard.clicked.connect(lambda: self.parent.switch_screen("leaderboard"))

        btn_home = QPushButton("Home")
        btn_home.clicked.connect(lambda: self.parent.switch_screen("welcome"))
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_retry)
        btn_layout.addWidget(btn_leaderboard)
        btn_layout.addWidget(btn_home)
        layout.addWidget(self.result_label)
        layout.addLayout(btn_layout)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        container.setLayout(layout)
        scroll.setWidget(container)
        outer_layout = QVBoxLayout()
        outer_layout.addWidget(scroll)
        self.setLayout(outer_layout)


    def set_results(self, wpm, accuracy, passage):

        self.wpm = wpm
        self.accuracy = accuracy
        self.passage = passage
        self.result_label.setText(
            f"Your Results\n\nWPM: {wpm:.2f}\nAccuracy: {accuracy:.2f}%"
        )

    def save_score(self):

        name, ok = QInputDialog.getText(self, "Save Score", "Enter your name:")
        if ok and name.strip():
            scores = load_leaderboard()
            scores.append({
                "name": name.strip(),
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "wpm": round(self.wpm, 2),
                "accuracy": round(self.accuracy, 2)
            })
            scores.sort(key=lambda x: x["wpm"], reverse=True)
            save_leaderboard(scores[:10])  # Keep top 10
            QMessageBox.information(self, "Saved", "Your score has been saved!")
            self.parent.switch_screen("leaderboard")
        else:
            QMessageBox.warning(self, "Invalid Name", "Please enter a valid name.")

class LeaderboardScreen(QWidget):

    def __init__(self, parent):

        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(15)
        self.title = QLabel("🏆 Leaderboard 🏆")
        self.title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Rank", "Name", "WPM", "Accuracy"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("alternate-background-color: #f0e6ff;")

        btn_back = QPushButton("Back")
        btn_back.clicked.connect(lambda: self.parent.switch_screen("welcome"))

        layout.addWidget(self.title)
        layout.addWidget(self.table)
        layout.addWidget(btn_back)
        self.setLayout(layout)

    def load_scores(self):
        scores = load_leaderboard()
        self.table.setRowCount(len(scores))
        for row, score in enumerate(scores):
            self.table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            self.table.setItem(row, 1, QTableWidgetItem(score["name"]))
            self.table.setItem(row, 2, QTableWidgetItem(str(score["wpm"])))
            self.table.setItem(row, 3, QTableWidgetItem(f"{score['accuracy']}%"))

class SettingsScreen(QWidget):

    def __init__(self, parent):

        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):

        layout = QVBoxLayout()
        layout.setContentsMargins(50, 40, 50, 40)
        layout.setSpacing(25)

        title = QLabel("Settings")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_light = QPushButton("Light Theme")
        btn_light.clicked.connect(lambda: self.parent.set_theme("light"))

        btn_dark = QPushButton("Dark Theme")
        btn_dark.clicked.connect(lambda: self.parent.set_theme("dark"))

        btn_back = QPushButton("Back")
        btn_back.clicked.connect(lambda: self.parent.switch_screen("welcome"))

        layout.addWidget(title)
        layout.addWidget(btn_light)
        layout.addWidget(btn_dark)
        layout.addWidget(btn_back)
        self.setLayout(layout)

def main():
    app = QApplication(sys.argv)
    window = TypingTestApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()