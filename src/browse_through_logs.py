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
import datetime

from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QWidget,
    QPushButton,
    QPlainTextEdit,
    QComboBox,
    QMessageBox,
    QInputDialog,
    QLineEdit
)

from PyQt5.QtWidgets import QGridLayout, QVBoxLayout

__version__ = "0.1"
path = '.'

all_dirs = sorted([
    i for i in os.listdir() if os.path.isdir(os.path.join(path, i)) \
                            and i != "✰ Yearly Capsule ✰"
])

all_data = {
    year: {
        create_datetime: data for create_datetime, data in zip(
            [
                datetime.datetime.fromtimestamp(
                    os.stat(
                        os.path.join(year, i)
                    ).st_ctime
                ) for i in os.listdir(
                    os.path.join(
                        year
                    )
                )
            ],
            [
                open(
                    os.path.join(
                        year, filepath
                        ), encoding='latin1'
                    ).read() for filepath in os.listdir(
                        os.path.join(
                            year
                            )
                        ) if filepath.split(
                        '.'
                        )[-1] not in [
                            'png', 'jpg', 'jpeg'
                        ] 
                ]
            )
        } for year in os.listdir(
            
        ) if year != "✰ Yearly Capsule ✰" and os.path.isdir(
            year
            )
}

annual_log_dir = os.path.join(path, "✰ Yearly Capsule ✰")

authorized_annual_log = {"layout": False, "text": False}


def format_byte(size: int, decimal_places: int = 3):
    """
    Formats a given size and outputs a string equivalent to B, KB, MB, or GB
    """
    if size < 1e03:
        return f"{round(size, decimal_places)} B"
    if size < 1e06:
        return f"{round(size / 1e3, decimal_places)} KB"
    if size < 1e09:
        return f"{round(size / 1e6, decimal_places)} MB"

    return f"{round(size / 1e9, decimal_places)} GB"


class HomeLayout(QWidget):
    def __init__(self, mainwindow, daily_log_class, annual_log_class):
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

        self.stat_button = QPushButton("Stats")
        
        self.year_combobox.currentTextChanged.connect(self.change_text)
        self.daily_log_button.clicked.connect(
            self.change_to_daily_log
        )
        self.annual_log_button.clicked.connect(
            self.change_to_annual_log
        )
        self.stat_button.clicked.connect(
            self.change_to_stat
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

        # self.layout.addWidget(self.stat_label, 1, 1)
        self.layout.addWidget(self.stat_button, 0, 1)

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
        self.daily_log_class.year = int(combobox_text)

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
        if not authorized_annual_log["layout"]:
            text, ok = QInputDialog().getText(
                self, "Password", "Enter Hex Password:"
            )
            if text == '790c03848c09f5e2ebaa702b4bd0d6db' and ok:
                self.mainwindow.change_layout(self.mainwindow.annuallog)
                authorized_annual_log["layout"] = True
            else:
                QMessageBox.about(
                    self, "Incorrect Password",
                    "AHAAAHaHAHAHHAHAH WRONG PASSWORD"
                )
        else:
            self.mainwindow.change_layout(self.mainwindow.annuallog)

    def change_to_stat(self):
        self.mainwindow.change_layout(self.mainwindow.stats_layout)
        

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
        self.refresh_logs_button = QPushButton("Refresh Logs")
        self.log_info = QLabel()

        self.home_button.clicked.connect(lambda: self.mainwindow.change_layout(self.mainwindow.home))
        self.help_button.clicked.connect(self.help_popup)
        self.next_log_button.clicked.connect(self.next_log)
        self.prev_log_button.clicked.connect(self.prev_log)
        self.first_log_button.clicked.connect(self.first_log)
        self.last_log_button.clicked.connect(self.last_log)
        self.refresh_logs_button.clicked.connect(self.refresh_logs)
        
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
        self.layout.addWidget(self.refresh_logs_button, 2, 3)

    def setup(self):
        self.mainwindow.setWindowTitle("Daily Log Browser")

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

    def refresh_logs(self):
        self.logs = []

        files = [
            os.path.join(path, str(self.year), i) \
            for i in os.listdir(str(self.year)) \
            if os.path.isfile(os.path.join(path, str(self.year), i))
        ]

        for file in files:
            with open(file, encoding='utf8') as file_read:
                content = file_read.read()
            self.logs.append(content)

        len_logs = len(self.logs)

        if len_logs == 0 or len_logs > 1:
            verbose = "logs"
        else:
            verbose = "log"
        
        self.hello_msg.setText(
            f"<h1>{len(self.logs)} {verbose} for {self.year}"
        )

        if len(self.logs) > 0:
            self.log_info.setText(f"<h2>Log 1/{len(self.logs)}")
        else:
            self.logs.append('No Logs for this year.')
            self.log_info.setText(f"<h2>Log 0/0")
        self.current_log = self.logs[0]
        self.log_msg.setPlainText(self.current_log)

        QMessageBox.about(
            self, "Refresh Successful",
            f"Successfully refreshed logs for {self.year}"
        )


class AnnualLogLayout(QWidget):
    def __init__(self, mainwindow):
        super().__init__()

        self.mainwindow = mainwindow

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # self.home_button = QPushButton("Home")

        # self.home_button.clicked.connect(lambda: self.mainwindow.change_layout(self.mainwindow.home))

        # self.layout.addWidget(self.home_button, 0, 0)

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
        # self.help_button.clicked.connect(self.help_popup)
        # self.next_log_button.clicked.connect(self.next_log)
        # self.prev_log_button.clicked.connect(self.prev_log)
        # self.first_log_button.clicked.connect(self.first_log)
        # self.last_log_button.clicked.connect(self.last_log)
        
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
        self.mainwindow.setWindowTitle("Annual Log Browser")


class StatLayout(QWidget):
    def __init__(self, mainwindow):
        super().__init__()

        self.mainwindow = mainwindow

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        bytes_total = 0
        bytes_daily = 0
        num_entries_daily = 0
        num_entries_total = 0
        for year in all_data.values():
            for day in year.values():
                bytes_total += len(day)
                num_entries_total += 1

                if year != "✰ Yearly Capsule ✰":
                    bytes_daily += len(day)
                    num_entries_daily += 1

        self.home_button = QPushButton("Home")
        self.title = QLabel("<h1>Statistics for all logs</h1>")

        self.bytes_label = QLabel(f"<h3>Total Bytes Written: {bytes_total} Bytes ({format_byte(bytes_total)})</h3>")
        self.avg_per_log = QLabel(f"<h3>Avg. Length of Logs: {round(bytes_daily / num_entries_daily, 2)} Bytes Daily Logs<br/></h3><h3 style=\"margin-left: 205px\">{f'{round((bytes_total - bytes_daily ) / (num_entries_total - num_entries_daily), 2)}' if num_entries_total - num_entries_daily != 0 else f'N/A'} Bytes Annual Logs</h3>")
        
        self.home_button.clicked.connect(lambda: self.mainwindow.change_layout(self.mainwindow.home))

        self.layout.addWidget(self.home_button, 0, 0)
        self.layout.addWidget(self.title, 1, 0)
        self.layout.addWidget(self.bytes_label, 2, 0)
        self.layout.addWidget(self.avg_per_log, 3, 0)
        
    def setup(self):
        self.mainwindow.setWindowTitle("A")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.resize(500, 500)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.dailylog = DailyLogLayout(self)
        self.annuallog = AnnualLogLayout(self)
        self.home = HomeLayout(self, self.dailylog, self.annuallog)
        self.stats_layout = StatLayout(self)
        self.layout.addWidget(self.home)
        self.layout.addWidget(self.dailylog)
        self.layout.addWidget(self.annuallog)
        self.layout.addWidget(self.stats_layout)

        self.layouts = (self.home, self.dailylog, self.annuallog, self.stats_layout)

        self.change_layout(self.home)

    def change_layout(self, layout):
        for l in self.layouts:
            l.hide()
        layout.show()
        layout.setup()



if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())
