# import sys
import logging
import qdarkstyle

from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit
from PyQt5.QtWidgets import QComboBox, QMessageBox
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QDesktopWidget

from sys import platform as _platform

from .main_interface import MainInterface
from ..func.session import Session
from ..func.login import GameLogin
from ..func import constants as constants


class LoginForm(QWidget):
    # LoginForm is derived from QWidget; there can be multiple inheritance
    def __init__(self):
        super().__init__()
        self.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
        
        user_w = QDesktopWidget().screenGeometry(-1).width()
        user_h = QDesktopWidget().screenGeometry(-1).height()
        self.resize(0.26*user_w, 0.12*user_h)

        layout = QGridLayout()

        label_name = self.create_qLabel('Username')
        self.lineEdit_username = QLineEdit()
        self.lineEdit_username.setPlaceholderText('Please enter your username')
        # addWidget(widget, row_number, col_number, row_span<opt>, col_span<opt>)
        layout.addWidget(label_name, 0, 0)
        layout.addWidget(self.lineEdit_username, 0, 1)

        label_password = self.create_qLabel('Password')
        self.lineEdit_password = QLineEdit()
        self.lineEdit_password.setEchoMode(QLineEdit.Password)
        output = self.lineEdit_password.text()
        self.lineEdit_password.setPlaceholderText('Please enter your password')
        layout.addWidget(label_password, 1, 0)
        layout.addWidget(self.lineEdit_password, 1, 1)

        label_platform = self.create_qLabel('Platform')
        combo_platform = QComboBox()
        # platforms = ["Choose your platform", "CN-iOS", "CN-Android", "International", "JP"]
        platforms = ["Choose your platform", "CN-iOS"]
        combo_platform.addItems(platforms)
        combo_platform.currentTextChanged.connect(self.update_server_box)
        layout.addWidget(label_platform, 2, 0)
        layout.addWidget(combo_platform, 2, 1)

        label_server = self.create_qLabel('Server')
        self.combo_server = QComboBox()
        self.combo_server.currentTextChanged.connect(self.update_server)
        layout.addWidget(label_server, 3, 0)
        layout.addWidget(self.combo_server, 3, 1)

        button_login = QPushButton('Login')
        button_login.clicked.connect(self.check_password)
        layout.addWidget(button_login, 5, 0, 1, 2)
        # set a gap between row3 and row5, i.e. an empty row4
        layout.setRowMinimumHeight(4, 0.03*user_h)

        self.setLayout(layout)
        self.setWindowTitle('Warship Girls Viewer Login')

    def create_qLabel(self, text):
        _str = '<font size="4"> ' + text + ' </font>'
        _res = QLabel(_str)
        return _res

    def update_server_box(self, text):
        servers = []
        self.combo_server.clear()
        # TODO: remove hardcoding
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
        try:
            res1 = account.first_login(_username, _password)
            res2 = account.second_login(self.server)
        except (KeyError, requests.exceptions.ReadTimeout) as e:
            logging.error(e)
            msg.setText("Logging failed.")
            msg.exec_()
            return

        if res1 == True and res2 == True:
            logging.info("Login Successfully...")
            msg.setText('Success')
            msg.exec_()
            msg.close()
            cookies = account.get_cookies()
            self.mi = MainInterface(self.server, self.channel, cookies)
            self.login_success()
        else:
            msg.setText("Incorrect Password.")
            msg.exec_()

    def login_success(self):
        self.mi.show()
        self.close()


# End of File