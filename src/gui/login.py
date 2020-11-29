import logging
import requests
import qdarkstyle

from PyQt5.QtCore import QSettings, QVariant
from PyQt5.QtWidgets import (
    QPushButton, QLabel, QLineEdit,
    QComboBox, QMessageBox, QCheckBox,
    QWidget, QDesktopWidget,
    QGridLayout
)

from src import data as wgr_data
from src.func.encryptor import Encryptor
from src.func.login import GameLogin
from src.func.session import Session
from src.func import constants as constants
from .main_interface import MainInterface


class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.qsettings = QSettings(wgr_data.get_qsettings_file(), QSettings.IniFormat)
        self.encryptor = Encryptor()
        self.key_filename = '.wgr.key'

        self.style_sheet = wgr_data.get_color_scheme()

        if self.qsettings.value("Login/checked") == 'true':
            self.qsettings.beginGroup('Login')
            name = self.qsettings.value('username')
            server = self.qsettings.value('server_text')
            platform = self.qsettings.value('platform_text')
            self.qsettings.endGroup()

            # Don't change the order
            self.init_name_field(name)
            self.init_password_field(self._get_password())
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
        self.init_ui_qsettings()

    # ================================
    # Initialization
    # ================================

    def init_ui_qsettings(self):
        user_w = QDesktopWidget().screenGeometry(-1).width()
        user_h = QDesktopWidget().screenGeometry(-1).height()
        self.init_login_button(user_h)
        self.resize(0.26 * user_w, 0.12 * user_h)
        self.setStyleSheet(self.style_sheet)
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
        platforms = ["Choose your platform", "CN-iOS", "CN-Android"]
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
        self.checkbox = QCheckBox('remember login info (secured by encryption)')
        self.checkbox.setChecked(checked)
        self.checkbox.stateChanged.connect(self.on_check_clicked)
        self.layout.addWidget(self.checkbox, 4, 1)

    def init_login_button(self, user_h):
        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.check_password)
        # set an empty gap row
        self.layout.addWidget(self.login_button, 6, 0, 1, 2)
        self.layout.setRowMinimumHeight(5, 0.03 * user_h)

    # ================================
    # General
    # ================================

    def create_qLabel(self, text):
        _str = '<font size="4"> ' + text + ' </font>'
        _res = QLabel(_str)
        return _res

    def login_success(self):
        self.mi.show()
        self.close()

    def _get_password(self):
        if wgr_data.is_key_exists(self.key_filename) and self.qsettings.contains('Login/password'):
            key = self.encryptor.load_key(wgr_data.get_key_path(self.key_filename))
            res = self.encryptor.decrypt_data(key, self.qsettings.value('Login/password')).decode("utf-8")
        else:
            res = ''
        return res

    # ================================
    # Events
    # ================================

    def on_check_clicked(self):
        if self.checkbox.isChecked():
            self.qsettings.beginGroup('Login')
            self.qsettings.setValue("checked", self.checkbox.isChecked())
            self.qsettings.setValue("server_text", self.combo_server.currentText())
            self.qsettings.setValue("platform_text", self.combo_platform.currentText())
            self.qsettings.setValue("username", self.lineEdit_username.text())
            self.qsettings.setValue("password", self._get_password())
            self.qsettings.endGroup()
        else:
            self.qsettings.remove("Login")
            wgr_data.del_key_file(self.key_filename)

    def update_server_box(self, text):
        servers = []
        self.combo_server.clear()
        if text == "CN-iOS":
            servers = ["列克星敦", "维内托"]
            self.channel = "100020"
        elif text == "CN-Android":
            servers = ["胡德", "俾斯麦", "昆西", "长春"]
        #     self.channel = "100015"
        # elif text == "International":
        #     servers = ["server1", "NOT TESTED!"]
        #     self.channel = "100060"
        # elif text == "JP":
        #     servers = ["server1", "server2", "NOT TESTED!"]
        #     self.channel = "100024"
        else:
            servers = ["N/A"]
            logging.warning("Login server is not chosen.")
        self.combo_server.addItems(servers)

    def update_server(self, text):
        if text == "列克星敦":
            self.server = "http://s101.jr.moefantasy.com/"
        elif text == "维内托":
            self.server = "http://s108.jr.moefantasy.com/"
        elif text == "胡德":
            self.server = "http://s2.jr.moefantasy.com/"
        elif text == "俾斯麦":
            self.server = "http://s4.jr.moefantasy.com/"
        elif text == "昆西":
            self.server = "http://s13.jr.moefantasy.com/"
        elif text == "长春":
            self.server = "http://s14.jr.moefantasy.com/"
        elif text == "":
            logging.warning("Server is not manually chosen.")
        else:
            logging.error("Invalid server name: {}".format(text))

    def check_password(self):

        def _login_failed():
            msg.setText("Login Failed: Probably due to bad server connection")
            msg.exec_()
            self.login_button.setEnabled(True)
            self.login_button.setText('Login')

        # TODO: #30
        self.login_button.setText('Connecting to server...')
        self.login_button.setEnabled(False)
        self.on_check_clicked()

        msg = QMessageBox()
        msg.setStyleSheet(self.style_sheet)
        msg.setWindowTitle("Info")

        sess = Session()
        account = GameLogin(constants.version, self.channel, sess, self.login_button)
        _username = self.lineEdit_username.text()
        _password = self.lineEdit_password.text()

        if wgr_data.is_key_exists(self.key_filename) == False:
            key = self.encryptor.gen_key()
            self.encryptor.save_key(key, wgr_data.get_key_path(self.key_filename))
        else:
            key = self.encryptor.load_key(wgr_data.get_key_path(self.key_filename))
        self.qsettings.setValue('Login/password', self.encryptor.encrypt_str(key, _password))

        try:
            res1 = account.first_login(_username, _password)
            res2 = account.second_login(self.server)
            self.login_button.setText('Loading and Initializing...')
        except (KeyError, requests.exceptions.ReadTimeout, AttributeError) as e:
            logging.error(f"LOGIN - {e}")
            _login_failed()
            return

        if res1 == True and res2 == True:
            logging.info("LOGIN - SUCCESS!")
            msg.setText('Login Success')
            msg.exec_()
            msg.close()
            self.mi = MainInterface(self.server, self.channel, account.get_cookies())
            self.login_success()
        else:
            _login_failed()

# End of File
