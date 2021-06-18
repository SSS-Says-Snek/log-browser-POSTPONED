"""
A simple log browser to browse my log entries I made through the years.
Code is super messy, just a note to future me who stumbles across this atrocity


First Created: Jun 9th, 2021
Version 0.1
Age: 13
"""

import glob

import os
import sys

from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QWidget,
    QPushButton,
    QPlainTextEdit,
    QComboBox,
    QMessageBox
)

from PyQt5.QtWidgets import QGridLayout, QVBoxLayout

__version__ = "0.1"
path = '.'

all_dirs = sorted([
    i for i in os.listdir() if os.path.isdir(os.path.join(path, i)) \
                            and i != "✰ Yearly Capsule ✰"
])
annual_log_dir = os.path.join(path, "✰ Yearly Capsule ✰")


class HomeLayout(QWidget):
    def __init__(self, mainwindow, daily_log_class):
        super().__init__()
        self.mainwindow = mainwindow
        self.layout = QGridLayout()
        self.daily_log_class = daily_log_class

        self.desc_str = (
            f"A GUI used to browse through my logs.<br/>Currently Unfinished<br/>"
            f"Version {__version__}"
        )

        self.title = QLabel("<h1>Log Browser</h1>")
        self.desc = QLabel(f"<h3>{self.desc_str}</h3>")
        self.year_label = QLabel("<h3>Year to Browse:</h3>")
        self.daily_log_button = QPushButton("Daily Logs", self)
        self.daily_log_button_label = QLabel("<h3>Click here to search:</h3>")
        self.annual_log_button = QPushButton("Annual Logs", self)
        self.annual_log_button_label = QLabel("<h3>Click here to view annual logs:</h3>")
        self.year_combobox = QComboBox(self)
        
        self.year_combobox.currentTextChanged.connect(self.change_text)
        self.daily_log_button.clicked.connect(
            self.change_to_daily_log
        )
        self.annual_log_button.clicked.connect(
            self.change_to_annual_log
        )

        self.year_combobox.addItems(all_dirs)

        self.layout.addWidget(self.title, 0, 0)
        self.layout.addWidget(self.desc, 1, 0)
        self.layout.addWidget(self.year_label, 2, 0)
        self.layout.addWidget(self.year_combobox, 2, 1)
        self.layout.addWidget(self.daily_log_button_label, 3, 0)
        self.layout.addWidget(self.daily_log_button, 3, 1)
        self.layout.addWidget(self.annual_log_button_label, 4, 0)
        self.layout.addWidget(self.annual_log_button, 4, 1)

        self.setLayout(self.layout)

    def setup(self):
        self.mainwindow.setWindowTitle("Home")

    def change_text(self, text):
        self.year_combobox.setCurrentText(text)
        self.year_combobox.adjustSize()
        self.daily_log_button.setText(f"Daily Logs for {text}")

    def change_to_daily_log(self):
        self.daily_log_class.logs = []

        combobox_text = str(self.year_combobox.currentText())

        files = [
            os.path.join(path, combobox_text, i) \
            for i in os.listdir(combobox_text) \
            if os.path.isfile(os.path.join(path, combobox_text, i))
        ]

        for file in files:
            with open(file, encoding='utf8') as file_read:
                content = file_read.read()
            self.daily_log_class.logs.append(content)

        len_logs = len(self.daily_log_class.logs)

        if len_logs == 0 or len_logs > 1:
            verbose = "logs"
        else:
            verbose = "log"
        
        self.daily_log_class.hello_msg.setText(
            f"<h1>{len(self.daily_log_class.logs)} {verbose} for {combobox_text}"
        )

        if len(self.daily_log_class.logs) > 0:
            self.daily_log_class.log_info.setText(f"<h2>Log 1/{len(self.daily_log_class.logs)}")
        else:
            self.daily_log_class.logs.append('No Logs for this year.')
            self.daily_log_class.log_info.setText(f"<h2>Log 0/0")
        self.daily_log_class.current_log = self.daily_log_class.logs[0]
        self.daily_log_class.log_msg.setPlainText(self.daily_log_class.current_log)

        self.mainwindow.change_layout(self.mainwindow.dailylog)

    def change_to_annual_log(self):
        QMessageBox.about(
            self, "E",
            "Not done kek"
        )
        

class DailyLogLayout(QWidget):
    def __init__(self, mainwindow):
        super().__init__()
        self.mainwindow = mainwindow

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.log_index = 0

        self.hello_msg = QLabel()
        self.log_msg = QPlainTextEdit()
        self.next_log_button = QPushButton("Next Log")
        self.prev_log_button = QPushButton("Previous Log")
        self.first_log_button = QPushButton("First Log")
        self.last_log_button = QPushButton("Last Log")
        self.home_button = QPushButton("Home")
        self.help_button = QPushButton("Help")
        self.log_info = QLabel()

        self.home_button.clicked.connect(lambda: self.mainwindow.change_layout(self.mainwindow.home))
        self.help_button.clicked.connect(self.help_popup)
        self.next_log_button.clicked.connect(self.next_log)
        self.prev_log_button.clicked.connect(self.prev_log)
        self.first_log_button.clicked.connect(self.first_log)
        self.last_log_button.clicked.connect(self.last_log)
        
        self.log_msg.setOverwriteMode(True)
        
        self.layout.addWidget(self.hello_msg, 0, 2)
        self.layout.addWidget(self.next_log_button, 3, 2)
        self.layout.addWidget(self.prev_log_button, 3, 1)
        self.layout.addWidget(self.first_log_button, 3, 0)
        self.layout.addWidget(self.last_log_button, 3, 3)
        self.layout.addWidget(self.home_button, 0, 0)
        self.layout.addWidget(self.help_button, 0, 1)
        self.layout.addWidget(self.log_msg, 1, 0, 1, 4)
        self.layout.addWidget(self.log_info, 2, 0, 1, 4)

    def setup(self):
        self.mainwindow.setWindowTitle("Log Browser")

    def next_log(self):
        if self.log_index + 1 < len(self.logs):
            self.log_index += 1
            self.current_log = self.logs[self.log_index]
        if self.logs[0] == 'No Logs for this year.':
            self.log_info.setText(f"<h2>Log 0/0</h2>")
        else:
            self.log_info.setText(f"<h2>Log {self.log_index+1}/{len(self.logs)}</h2>")
        self.log_msg.setPlainText(self.current_log)

    def prev_log(self):
        if self.log_index - 1 >= 0:
            self.log_index -= 1
        if self.logs[0] == 'No Logs for this year.':
            self.log_info.setText(f"<h2>Log 0/0</h2>")
        else:
            self.log_info.setText(f"<h2>Log {self.log_index+1}/{len(self.logs)}</h2>")

        self.current_log = self.logs[self.log_index]
        self.log_msg.setPlainText(self.current_log)

    def first_log(self):
        self.log_index = 0
        self.current_log = self.logs[self.log_index]

        self.log_info.setText(f"<h2>Log 1/{len(self.logs)}</h2>")
        self.log_msg.setPlainText(self.current_log)

    def last_log(self):
        self.log_index = len(self.logs) - 1
        self.current_log = self.logs[self.log_index]

        self.log_info.setText(f"<h2>Log {len(self.logs)}/{len(self.logs)}</h2>")
        self.log_msg.setPlainText(self.current_log)

    def help_popup(self):
        help_messagebox = QMessageBox()
        help_messagebox.setIcon(QMessageBox.Question)
        help_messagebox.about(
            self, "Help",
            "Press the \"Previous Log\" button to view the previous log.\n"
            "Press the \"Next Log\" button to view the next log.\n"
            "Press the \"First Log\" button to view the first log.\n"
            "Press the \"Last Log\" button to view the last log.\n"
            "Press the \"Home\" button to return to the home screen.\n\n"
            "Yes, this was supposed to display the first log, but "
            "I couldn't figure it out. Classic example of "
            "\"It's a feature, not a bug\" lol"
        )


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.resize(500, 500)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.dailylog = DailyLogLayout(self)
        self.home = HomeLayout(self, self.dailylog)
        self.layout.addWidget(self.home)
        self.layout.addWidget(self.dailylog)

        self.layouts = (self.home, self.dailylog)

        self.change_layout(self.home)

    def change_layout(self, layout):
        for l in self.layouts:
            l.hide()
        layout.show()
        layout.setup()



if __name__ == "__main__":
    app = QApplication(sys.argv)

    mw = MainWindow()
    mw.show()

    sys.exit(app.exec_())
