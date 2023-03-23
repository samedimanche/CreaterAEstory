import sys, os
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import QDate, Qt, QTimer
# from PyQt5.QtGui import QIcon
import subprocess
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
# import requests
from bs4 import BeautifulSoup
import json
headers = {"User-Agent" : 'Mozilla/5.0'}
class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # rewrite test.txt
        with open("test.txt", "w") as f:
            f.write("")
        # create checkboxes for the left and right sides
        self.left_checks = [QCheckBox("Krasnoyarsk"), QCheckBox("Moscow"), QCheckBox("Khabarovsk"), QCheckBox("Vladivostok"), QCheckBox("Blagoveshensk"), QCheckBox("Irkutsk")]
        self.right_checks = [QCheckBox("Thailand"), QCheckBox("Turkish"), QCheckBox("Egypt"), QCheckBox("UAE"), QCheckBox("Venezuela"), QCheckBox("Cuba"), QCheckBox("Vietnam")]

        self.calendar = QCalendarWidget()
        default_date = QDate.currentDate().addDays(7)
        self.calendar.setSelectedDate(default_date)

        label1 = QLabel("Установить сумму (до 3 цифр первых, 3 нуля подставляются автоматический)")
        label1.setFont(QFont("Arial", 15))
        label1.setStyleSheet("color:#000;")
        # label1.setAlignment(QtCore.Qt.AlignCenter)
        label2 = QLabel("Выполнение")
        label2.setFont(QFont("Arial", 15))
        label2.setAlignment(QtCore.Qt.AlignCenter)
        label2.setStyleSheet('color: #000;')

        # create a progress bar widget
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("""
        QProgressBar {
            border: 2px solid grey;
            border-radius: 10px;
            text-align: center;
            background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                              stop: 0 #fff, stop: 1 #fff);

        }
        QProgressBar::chunk {
            background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                              stop: 0 #66CCFF, stop: 1 #0099FF);
            border-radius: 10px;
        }
        """)

        # create a spin box widget
        self.spin_box = QSpinBox(self)
        self.spin_box.setRange(0, 999)
        self.spin_box.setValue(0)
        self.spin_box.setFixedSize(100, 50)
        self.spin_box.setStyleSheet("""
            QSpinBox {
                border: 2px solid gray;
                border-radius: 4px;
                font-size: 16px;
                padding: 2px;
            }
            QSpinBox:hover {
                border-color: blue;
            }
            QSpinBox::up-button {
                width: 20px;
                height: 20px;
                subcontrol-origin: padding;
                subcontrol-position: top right;
                border: 2px solid gray;
                border-top-right-radius: 4px;
            }
            QSpinBox::down-button {
                width: 20px;
                height: 20px;
                subcontrol-origin: padding;
                subcontrol-position: bottom right;
                border: 2px solid gray;
                border-bottom-right-radius: 4px;
            }
            QSpinBox::up-arrow {
                image: url(up_arrow.png);
            }
            QSpinBox::down-arrow {
                image: url(down_arrow.png);
            }
        """)

        # self.spin_box.setFont(QFont("Arial", 20))

        qhbox_for_spin_and_label1=QHBoxLayout()
        qhbox_for_spin_and_label1.addWidget(label1)
        qhbox_for_spin_and_label1.setSpacing(25)
        qhbox_for_spin_and_label1.addWidget(self.spin_box)
        qhbox_for_spin_and_label1.addStretch(1)

        # create a vertical layout for the calendar and spin box
        self.calendar_layout = QVBoxLayout()
        self.calendar_layout.addWidget(self.calendar)
        self.calendar_layout.addLayout(qhbox_for_spin_and_label1)

        # create a button
        button = QPushButton("Start")
        button.setFixedWidth(200)  # set the width of the button
        button.setFixedHeight(100)
        button.setStyleSheet('''
            QPushButton {
                background-color: #4CAF50;
                border-radius: 10px;
                color: white;
                font-size: 16px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3e8e41;
            }
            QPushButton:pressed {
                background-color: #2c6224;
            }
        ''')
        button.clicked.connect(self.handleButton)

        # create a button
        clear_button = QPushButton("Очистить файл\nот ссылок")
        clear_button.setFixedWidth(200)  # set the width of the button
        clear_button.setFixedHeight(100)
        clear_button.setStyleSheet('''
            QPushButton {
                background-color: #FF0000;
                border-radius: 10px;
                color: white;
                font-size: 16px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #D2042D;
            }
            QPushButton:pressed {
                background-color: #C41E3A;
            }
        ''')
        clear_button.clicked.connect(self.clear_file_button)

        clera_button_and_start_button = QHBoxLayout()
        clera_button_and_start_button.addWidget(button)
        clera_button_and_start_button.addWidget(clear_button)

        # create a vertical layout for the label, progress bar, and button
        self.bottom_layout = QVBoxLayout()
        self.bottom_layout.addWidget(label2)
        self.bottom_layout.addWidget(self.progress_bar)
        self.bottom_layout.addLayout(clera_button_and_start_button)
        self.bottom_layout.addStretch(1)

        # create a horizontal layout for the top checkboxes
        self.top_layout = QHBoxLayout()
        self.left_col_layout = QVBoxLayout()
        for check in self.left_checks:
            check.setGeometry(10, 10, 100, 30)
            check.setStyleSheet("""
            QCheckBox::indicator {
                width: 25px;
                height: 25px;
            }
            QCheckBox::indicator:checked {
                image: url(checked.png);
            }
            QCheckBox::indicator:unchecked {
                image: url(unchecked.png);
            }
            """)
            self.left_col_layout.addWidget(check)
        self.top_layout.addLayout(self.left_col_layout)
        self.right_col_layout = QVBoxLayout()
        for check in self.right_checks:
            check.setGeometry(10, 10, 100, 30)
            check.setStyleSheet("""
            QCheckBox::indicator {
                width: 25px;
                height: 25px;
            }
            QCheckBox::indicator:checked {
                image: url(checked.png);
            }
            QCheckBox::indicator:unchecked {
                image: url(unchecked.png);
            }
            """)
            self.right_col_layout.addWidget(check)
        self.top_layout.addLayout(self.right_col_layout)

        # create a vertical layout to combine the calendar layout and bottom layout
        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.calendar_layout)
        self.main_layout.addLayout(self.bottom_layout)

        self.setLayout(self.main_layout)
        self.setGeometry(500, 120, 400, 400)
        self.setWindowTitle('TinkoffTravel')
        self.show()
        # self.showMaximized()  # set the window to full screen

    def clear_file_button(self):
        with open("test.txt", "w") as f:
            f.write("")

    def handleButton(self):
        if hasattr(self, 'vbox'):

            self.link_button_ready.close()
            self.link_button_yet.close()
            self.link_cheqbox_links.close()
            self.line_edit_links.close()
            self.link_label_links.close()
            self.new_secondbutton.close()
        if hasattr(self, 'hboxFirst'):
            old_hboxFirst = self.hboxFirst
            self.main_layout.removeItem(old_hboxFirst)
            old_hboxFirst.deleteLater()
            self.new_button.close()
            self.new_button1.close()
            self.len_links.close()

        # create a new button
        # get QCheckBox values

        checked_left = []
        checked_right = []
        self.list_links_forcreate_AE=[]
        self.list_links_addfunction=[]

        for check in self.left_checks:
            if check.isChecked():
                checked_left.append(check.text())
        for check in self.right_checks:
            if check.isChecked():
                checked_right.append(check.text())

        self.date = self.calendar.selectedDate()
        # get the formatted string representation of the selected date
        self.date_from = self.date.toString("dd.MM.yyyy")
        # get the value of the spin box and store it in a variable
        self.price = self.spin_box.value()

        cityRus = {"Krasnoyarsk": 37, "Moscow": 2, "Khabarovsk": 80, "Vladivostok": 19, "Blagoveshensk": 15,
                   "Irkutsk": 28}
        cityOutside = {"Thailand": 87, "Turkish": 92, "Egypt": 29, "UAE": 68, "Venezuela": 21, "Cuba": 48,
                       "Vietnam": 22}
        lister = []
        url_list = []
        if int(self.price) > 0 and int(len(checked_left)) > 0 and int(len(checked_right)) > 0:
            def url_parser(date_from, price):
                for i in range(len(checked_left)):
                    for j in range(len(checked_right)):
                        from_city = checked_left[i]
                        to_city = checked_right[j]
                        from_country=str()
                        to_country = str()
                        if from_city in cityRus:
                            from_country=str(cityRus[from_city])
                        if to_city in cityOutside:
                            to_country=str(cityOutside[to_city])
                        URL = f"https://tinkoff.travelata.ru/search#?fromCity={from_country}&toCountry={to_country}" \
                              f"&dateFrom={date_from}" \
                              f"&dateTo={date_from}&nightFrom=8&nightTo=15" \
                              f"&adults=2&hotelClass=all&meal=all&priceFrom=6000&priceTo={price}000&sid=1px7n2x8d5&sort=priceUp&f_noScore=true"
                        url_list.append(URL)

            url_parser(self.date_from, self.price)

            def link_parser(i):
                driver = webdriver.Chrome()
                URL = i
                driver.minimize_window()
                driver.get(URL)
                time.sleep(5)
                link = list(driver.find_elements(by=By.CLASS_NAME, value="serpHotelCard__btn"))

                for links in range(0, int(len(link))):
                    link[links].click()
                    window_after = driver.window_handles[1]
                    driver.switch_to.window(window_after)
                    # current_url_for_iterators = (lambda x: x[:x.find("&dateFrom=") + len("&dateFrom=")+10] if x.find("&dateFrom=") != -1 else x)(driver.current_url)
                    # print(current_url_for_iterators)
                    # listre_for_iterators = [(lambda x: x[:x.find("&dateFrom=") + 10] if x.find("&dateFrom=") != -1 else x)(url) for url in lister]
                    # print(listre_for_iterators)
                    # if current_url_for_iterators not in listre_for_iterators:
                    lister.append(driver.current_url)
                    with open("test.txt", "a") as f:
                        f.write(driver.current_url + "\n")
                    driver.close()
                    window_after = driver.window_handles[0]
                    driver.switch_to.window(window_after)

                    # time.sleep(1)
                driver.close()
                driver.quit()

            for i in range(int(len(url_list))):
                link_parser(url_list[i])
                progress = int((i + 1) / len(url_list) * 100)
                self.progress_bar.setValue(progress)
                QApplication.processEvents()  # Update the GUI
                # Simulate some processing time
                time.sleep(0.5)

            self.len_links = QLabel(
                f'Найдено: <font color="red">{(lambda tur: f"{len(lister)}</font> " + ("тур" if len(lister) == 1 else "тура" if 2 <= len(lister) <= 4 else "туров"))(lister)}')
            self.len_links.setFont(QFont("Arial", 15))

            self.new_button = QPushButton("Open file")
            self.new_button.setFixedWidth(200)  # set the width of the button
            self.new_button.setFixedHeight(100)
            self.new_button.setStyleSheet('''
            QPushButton {
                background-color: #fff;
                border-radius: 10px;
                color: black;
                font-size: 16px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #F0FFFF;
            }
            QPushButton:pressed {
                background-color: #00FFFF;
            }
        ''')
            self.new_button.clicked.connect(self.handleNewButton)

            self.new_button1 = QPushButton("Продолжить")
            self.new_button1.setFixedWidth(200)  # set the width of the button
            self.new_button1.setFixedHeight(100)
            self.new_button1.setStyleSheet('''
            QPushButton {
                background-color: #7FFFD4;
                border-radius: 10px;
                color: black;
                font-size: 16px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #AFE1AF;
            }
            QPushButton:pressed {
                background-color: #50C878;
            }
        ''')
            self.new_button1.clicked.connect(self.handleNewSecondButton)

            self.hboxFirst = QHBoxLayout()
            self.hboxFirst.addWidget(self.new_button)
            self.hboxFirst.addWidget(self.len_links)
            self.hboxFirst.setSpacing(50)
            self.hboxFirst.addWidget(self.new_button1)
            self.hboxFirst.addStretch(1)

            # add the new button to the layout

            self.layout().addLayout(self.hboxFirst)

            # self.layout().addLayout(hboxFirst.setAlignment(QtCore.Qt.AlignCenter))
        else:
            QMessageBox.warning(self, "Warning", "Пожалуйста, проверьте, что сумма больше, чем 0,\nвыбран ли город вылета и страна прилёта")
    def handleNewButton(self):
        # open the file with the default text editor
        try:
            subprocess.run(["open", "-a", "TextEdit", "test.txt"])  # for macOS
        except FileNotFoundError:
            subprocess.run(["notepad.exe", "test.txt"])

    def handleNewSecondButton(self):
        if hasattr(self, 'vbox'):
            old_vbox = self.vbox
            self.main_layout.removeItem(old_vbox)
            old_vbox.deleteLater()
            self.link_button_ready.close()
            self.link_button_yet.close()
            self.link_cheqbox_links.close()
            self.line_edit_links.close()
            self.link_label_links.close()
            self.new_secondbutton.close()

        # Create QLabel with text "link"
        self.link_label_links = QLabel('Добавьте ссылки на туры в поле из которых нужно\n сделать видео или поставить галочку "Создать из всех"')
        self.link_cheqbox_links = QCheckBox("Создать из всех")
        self.link_cheqbox_links.setGeometry(10, 10, 100, 30)
        self.link_cheqbox_links.setStyleSheet("""
        QCheckBox::indicator {
            width: 25px;
            height: 25px;
        }
        QCheckBox::indicator:checked {
            image: url(checked.png);
        }
        QCheckBox::indicator:unchecked {
            image: url(unchecked.png);
        }
        """)

        # button for loop
        self.link_button_ready = QPushButton("Готово/Создать")
        self.link_button_ready.setFixedSize(200,50)
        self.link_button_ready.setStyleSheet('''
            QPushButton {
                background-color: #7FFFD4;
                border-radius: 10px;
                color: black;
                font-size: 16px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #AFE1AF;
            }
            QPushButton:pressed {
                background-color: #50C878;
            }
        ''')
        self.link_button_ready.clicked.connect(self.create_link_list)

        self.link_button_yet= QPushButton("Добавить ещё ссылку")
        self.link_button_yet.setFixedSize(250,50)
        self.link_button_yet.setStyleSheet('''
            QPushButton {
                background-color: #FFBF00;
                border-radius: 10px;
                color: black;
                font-size: 16px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #F4BB44;
            }
            QPushButton:pressed {
                background-color: #FFAC1C;}
        ''')
        self.link_button_yet.clicked.connect(self.add_link_list)

        # Create QLineEdit and two small QPushButtons under the QLabel field
        self.line_edit_links = QLineEdit()
        self.line_edit_links.setFixedSize(150, 50)
        self.line_edit_links.setStyleSheet("border-radius: 5px; border: 2px solid gray; color: black;")
        self.line_edit_links.setFont(QFont("Arial", 10))

        # create a new button open links
        self.new_secondbutton = QPushButton("Open links")
        self.new_secondbutton.setFixedWidth(200)  # set the width of the button
        self.new_secondbutton.setFixedHeight(100)
        self.new_secondbutton.setStyleSheet('''
            QPushButton {
                background-color: #fff;
                border-radius: 10px;
                color: black;
                font-size: 16px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #F0FFFF;
            }
            QPushButton:pressed {
                background-color: #00FFFF;
            }
        ''')
        self.new_secondbutton.clicked.connect(self.open_links)

        links_layout_buttons = QVBoxLayout()
        links_layout_buttons.addWidget(self.link_cheqbox_links)
        links_layout_buttons.addWidget(self.link_button_ready)

        # create a horizontal layout for the label and line edit
        links_layout = QVBoxLayout()
        links_layout.addWidget(self.link_label_links)
        links_layout.addWidget(self.line_edit_links)
        links_layout.addWidget(self.link_button_yet)

        # create a vertical layout for the button and links layout
        self.vbox = QHBoxLayout()
        self.vbox.addWidget(self.new_secondbutton)
        self.vbox.addLayout(links_layout)
        self.vbox.addLayout(links_layout_buttons)

        # add the layout and other widgets to the main layout
        layout = self.layout()
        layout.addLayout(self.vbox)

    def open_links(self):
        # open links in a new tab
        with open("test.txt",'r') as f:
            for line in f:
                webbrowser.open_new_tab(line.strip())
    def create_link_list(self):
        if self.link_cheqbox_links.isChecked():
            with open("test.txt", 'r') as f:
                for line in f:
                    self.list_links_forcreate_AE.append(line.strip())
        else:
            for line in self.list_links_addfunction:
                self.list_links_forcreate_AE.append(line)

        if int(len(self.list_links_forcreate_AE))<=0:
            QMessageBox.warning(self, "Warning", "Пожалуйста, проверьте, что вы поставили галочку в чекбокс\nили добавьте ссылки на туры в поле")
        else:
            self.get_json_for_AE(self.list_links_forcreate_AE)

    def add_link_list(self):
        if self.line_edit_links.text()!="":
            self.list_links_addfunction.append(self.line_edit_links.text())
            self.line_edit_links.clear()
        else:
            QMessageBox.warning(self, "Warning", "Пожалуйста, добавьте ссылки на туры в поле")

    # this code for AE story creater
    def is_ae_running(self):
        for proc in os.popen('tasklist').readlines():
            if 'AfterFX.exe' in proc:
                return True
            else:
                return False

    def loop_for_AEStory(self):

        for i in range(int(len(self.list_links_forcreate_AE))):
            self.a-=1
            if self.is_ae_running():
                pass
            else:
                os.startfile("F:/whatsaap/mainmainss.aep")
            urls_ae=self.list_links_forcreate_AE[i]
            url = urls_ae
            driverzz = webdriver.Chrome()
            driverzz.minimize_window()
            # get information from site_link for create AE template
            driverzz.get(url)
            time.sleep(0.2)
            html = driverzz.page_source
            soup = BeautifulSoup(html, "html.parser")
            start_index = url.find("&dateFrom=") + len("&dateFrom=")
            four_characters = url[start_index:start_index + 5]
            city_direct = soup.find('div', {"class": "resortName"}).text.strip().split(', ')[1]
            country_nameExp = soup.find('div', {"class": "resortName"}).text.strip().split(',')[0]
            link = (soup.find('span', {"class": "hotelTour__nights-in-tour"}).text.strip()).replace(",", "")
            price_text = soup.find('div', {"class": "hotelTour__price-block__btn"}).text.strip().split(' руб.')[0]
            # extract data from website
            # create a dictionary to store the data
            data = {
                "four_characters": four_characters,
                "city_direct": city_direct,
                "country_nameExp": country_nameExp,
                "link": link,
                "price_text": price_text
            }
            # write the data to a JSON file
            with open(f"data.json", "w") as outfile:
                json.dump(data, outfile)
            driverzz.quit()
            while not self.create_next_AEstory.isDown():
                app.processEvents()  # wait for button press
            self.create_next_AEstory.setDown(False)
            self.link_label_links.setText(f"Ещё <font color=\"red\">{self.a}</font> нажатия для создания всех видео")# reset button state
            self.link_label_links.setFont(QFont("Arial", 15))
        app.exit()
        # app.exit()
        # self.exit_from_program = QPushButton("Выйти")
        # self.exit_from_program.setFixedSize(150, 100)
        # self.exit_from_program.clicked.connect(self.exit_from_program)
        # self.layout().addWidget(self.exit_from_program)


    def get_json_for_AE(self, list_links_forcreate_AE):
        # self.create_next_AEstory.clicked.connect(self.create_next_AEstory)

        self.create_next_AEstory = QPushButton("Создать\nследующее видео")
        self.create_next_AEstory.setFixedSize(150, 100)
        self.create_next_AEstory.setStyleSheet('''
            QPushButton {
                background-color: #7FFFD4;
                border-radius: 10px;
                color: black;
                font-size: 16px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #AFE1AF;
            }
            QPushButton:pressed {
                background-color: #50C878;
            }
        ''')

        self.a=int(len(list_links_forcreate_AE))
        # self.link_label_links = QLabel(f'Ещё {self.len_list_links_forcreate_AE} нажатия для создания всех видео')
        self.link_label_links = QLabel(f'Ещё <font color=\"red\">{self.a}</font> нажатия для создания всех видео и выхода')
        self.link_label_links.setFont(QFont("Arial", 15))

        # setAlignment(QtCore.Qt.AlignCenter)
        self.create_next_AEstory.clicked.connect(lambda: self.create_next_AEstory.setDown(True))

        righthbox = QHBoxLayout()
        righthbox.addWidget(self.create_next_AEstory)
        righthbox.addWidget(self.link_label_links)

        self.layout().addLayout(righthbox)
        # self.layout().addWidget(self.create_next_AEstory)
        # self.layout().addWidget(self.link_label_links)
        self.loop_for_AEStory()

    # def exit_from_program(self):
    #     app.exit()

        app.exit()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
