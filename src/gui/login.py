# import sys
import logging
import requests
import qdarkstyle

from PyQt5.QtCore import QSettings, QVariant
from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit
from PyQt5.QtWidgets import QComboBox, QMessageBox, QCheckBox
from PyQt5.QtWidgets import QWidget, QDesktopWidget
from PyQt5.QtWidgets import QGridLayout

from sys import platform as _platform

from .main_interface import MainInterface
from ..func.session import Session
from ..func.login import GameLogin
from ..func import constants as constants
from ..func import data as wgr_data


class LoginForm(QWidget):
    # LoginForm is derived from QWidget; there can be multiple inheritance
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.settings = QSettings(wgr_data.get_settings_file(), QSettings.IniFormat)

        if self.settings.value("Login/checked") == 'true':
            self.settings.beginGroup('Login')
            name = self.settings.value('username')
            pswd = self.settings.value('password')
            server = self.settings.value('server_text')
            platform = self.settings.value('platform_text')
            self.settings.endGroup()
            # Don't change the order
            self.init_name_field(name)
            self.init_password_field(pswd)
            self.init_server_field(server)
            self.init_platform_field(platform)
            self.init_checkbox(True)
        else:
            self.init_name_field()
            self.init_password_field()
            self.init_platform_field()
            self.init_server_field()
            self.init_checkbox()

        self.setLayout(self.layout)
        self.init_ui_settings()

    def init_ui_settings(self):
        self.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))       
        user_w = QDesktopWidget().screenGeometry(-1).width()
        user_h = QDesktopWidget().screenGeometry(-1).height()
        self.resize(0.26*user_w, 0.12*user_h)
        self.init_login_button(user_h)
        self.setWindowTitle('Warship Girls Viewer Login')

    def init_name_field(self, text=''):
        label_name = self.create_qLabel('Username')
        self.lineEdit_username = QLineEdit()
        self.lineEdit_username.setClearButtonEnabled(True)

        if text == '':
            self.lineEdit_username.setPlaceholderText('Please enter your username')
        else:
            self.lineEdit_username.setText(text)

        # addWidget(widget, row_number, col_number, row_span<opt>, col_span<opt>)
        self.layout.addWidget(label_name, 0, 0)
        self.layout.addWidget(self.lineEdit_username, 0, 1)

    def init_password_field(self, text=''):
        label_password = self.create_qLabel('Password')
        self.lineEdit_password = QLineEdit()
        self.lineEdit_password.setClearButtonEnabled(True)
        self.lineEdit_password.setEchoMode(QLineEdit.Password)

        if text == '':
            self.lineEdit_password.setPlaceholderText('Please enter your password')
        else:
            self.lineEdit_password.setText(text)

        self.layout.addWidget(label_password, 1, 0)
        self.layout.addWidget(self.lineEdit_password, 1, 1)

    def init_platform_field(self, text=''):
        label_platform = self.create_qLabel('Platform')
        self.combo_platform = QComboBox()
        # platforms = ["Choose your platform", "CN-iOS", "CN-Android", "International", "JP"]
        platforms = ["Choose your platform", "CN-iOS"]
        self.combo_platform.addItems(platforms)
        self.combo_platform.currentTextChanged.connect(self.update_server_box)

        if text == '':
            pass
        else:
            self.combo_platform.setCurrentText(text)      

        self.layout.addWidget(label_platform, 2, 0)
        self.layout.addWidget(self.combo_platform, 2, 1)

    def init_server_field(self, text=''):
        label_server = self.create_qLabel('Server')
        self.combo_server = QComboBox()
        self.combo_server.currentTextChanged.connect(self.update_server)

        if text == '':
            pass
        else:
            self.combo_server.setCurrentText(text)

        self.layout.addWidget(label_server, 3, 0)
        self.layout.addWidget(self.combo_server, 3, 1)

    def init_checkbox(self, checked=False):
        self.checkbox = QCheckBox('remember login info')
        self.checkbox.setChecked(checked)
        self.checkbox.stateChanged.connect(self.on_check_clicked)
        self.layout.addWidget(self.checkbox, 4, 1)

    def init_login_button(self, user_h):
        button_login = QPushButton('Login')
        button_login.clicked.connect(self.check_password)
        self.layout.addWidget(button_login, 6, 0, 1, 2)
        # set a gap between row3 and row5, i.e. an empty row4
        self.layout.setRowMinimumHeight(5, 0.03*user_h)

    def create_qLabel(self, text):
        _str = '<font size="4"> ' + text + ' </font>'
        _res = QLabel(_str)
        return _res

    def login_success(self):
        # self.settings.endGroup()
        self.mi = MainInterface(self.server, self.channel, cookies)
        self.mi.show()
        self.close()


    # ================================
    # Events
    # ================================


    def on_check_clicked(self):
        self.settings.beginGroup('Login')
        self.settings.setValue("checked", self.checkbox.isChecked())
        self.settings.setValue("server_text", self.combo_server.currentText())
        self.settings.setValue("platform_text", self.combo_platform.currentText())
        self.settings.setValue("username", self.lineEdit_username.text())
        self.settings.setValue("password", self.lineEdit_password.text())
        self.settings.endGroup()

    def update_server_box(self, text):
        servers = []
        self.combo_server.clear()
        if text == "CN-iOS":
            servers = ["列克星敦", "维内托"]
            self.channel = "100020"
        # elif text == "CN-Android":
        #     servers = ["胡德", "俾斯麦", "昆西", "长春", "NOT TESTED!"]
        #     self.channel = "100015"
        # elif text == "International":
        #     servers = ["server1", "NOT TESTED!"]
        #     self.channel = "100060"
        # elif text == "JP":
        #     servers = ["server1", "server2", "NOT TESTED!"]
        #     self.channel = "100024"
        else:
            servers = ["N/A"]
            logging.warn("Login server is not chosen.")
        self.combo_server.addItems(servers)

    def update_server(self, text):
        if text == "列克星敦":
            self.server = "http://s101.jr.moefantasy.com/"
        elif text == "维内托":
            self.server = "http://s108.jr.moefantasy.com/"

    def check_password(self):
        msg = QMessageBox()
        msg.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
        msg.setWindowTitle("Info")

        sess = Session()
        account = GameLogin(constants.version, self.channel, sess)
        # TODO: store user info securely
        _username = self.lineEdit_username.text()
        _password = self.lineEdit_password.text()
        self.on_check_clicked()
        # try:
        #     res1 = account.first_login(_username, _password)
        #     res2 = account.second_login(self.server)
        # except (KeyError, requests.exceptions.ReadTimeout, AttributeError) as e:
        #     logging.error(e)
        #     msg.setText("Logging failed.")
        #     msg.exec_()
        #     return
        res1 = res2 = True

        if res1 == True and res2 == True:
            logging.info("Login Successfully...")
            msg.setText('Success')
            msg.exec_()
            msg.close()
            cookies = account.get_cookies()
            self.login_success()
        else:
            msg.setText("Incorrect Password.")
            msg.exec_()


# End of File