import logging
import requests
import threading
import time

from PyQt5.QtCore import QSettings, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import (
    QPushButton, QLabel, QLineEdit, QComboBox, QCheckBox, QWidget,
    QGridLayout, QVBoxLayout
)

from src import data as wgr_data
from src.exceptions.custom import InterruptExecution
from src.exceptions.wgr_error import WarshipGirlsExceptions
from src.func.encryptor import Encryptor
from src.func.login import GameLogin
from src.func.session import GameSession
from src.func import constants as constants
from src.func.version_check import VersionCheck
from src.func.worker import CallbackWorker
from src.utils import get_user_resolution, open_disclaimer, popup_msg, get_app_version
from .main_interface import MainInterface


def create_label(text: str):
    _str = '<font size="4"> ' + text + ' </font>'
    _res = QLabel(_str)
    return _res


class LoginForm(QWidget):
    sig_login = pyqtSignal()

    def __init__(self):
        super().__init__()
        VersionCheck(self)

        self.sig_login.connect(self.start_login)
        self.qsettings = QSettings(wgr_data.get_qsettings_file(), QSettings.IniFormat)
        self.encryptor = Encryptor()
        self.key_filename = '.wgr.key'
        self.channel = ""
        self.server = ""
        self.mi = None
        self.res1 = False
        self.res2 = False

        self.lineEdit_username = QLineEdit()
        self.lineEdit_password = QLineEdit()
        self.combo_platform = QComboBox()
        self.combo_server = QComboBox()
        self.check_disclaimer = QCheckBox('I have read and understood')
        # TODO? trailing space
        # To limit the trailing space of the checkbox text with max width; still, there is ~2 whitespaces width space presents
        # set text all in label would cause user unable to click text to toggle checkbox; differs from other checkbox, (bad design IMO)
        user_w, _ = get_user_resolution()
        self.check_disclaimer.setMaximumWidth(int(0.083 * user_w))
        self.check_save = QCheckBox('Store login info locally with encryption')
        self.check_auto = QCheckBox('Auto login on the application start')
        self.login_button = QPushButton('Login')

        self.container = QWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.container)
        self.layout = QGridLayout(self.container)

        self.init_ui()
        self.setLayout(main_layout)

        self.auto_start()

    def auto_start(self):
        if self.qsettings.value("Login/auto") == "true":
            # QThread cannot handle exceptions for this one
            try:
                self.login_button.setEnabled(False)  # in case user manually log-in
                self.check_auto.setText('!! Login auto starts in 5 seconds. Uncheck to pause !!')
                threading.Thread(target=self.wait_five_seconds).start()
            except InterruptExecution:
                pass
        else:
            pass

    # ================================
    # Initialization
    # ================================

    def init_ui(self):
        if self.qsettings.value("Login/save") == 'true':
            self.qsettings.beginGroup('Login')
            name = self.qsettings.value('username')
            server = self.qsettings.value('server_text')
            platform = self.qsettings.value('platform_text')
            disclaimer = self.qsettings.value('disclaimer')
            auto_login = self.qsettings.value('auto')
            self.qsettings.endGroup()

            # Don't change the order
            self.init_name_field(name)
            self.init_password_field(self._get_password())
            self.init_server_field(server)
            self.init_platform_field(platform)
            if disclaimer == "true":
                self.init_check_disclaimer(True)
            else:
                self.init_check_disclaimer(False)
            self.init_check_save(True)
            if auto_login == "true":
                self.init_check_auto(True)
            else:
                self.init_check_auto(False)
        else:
            self.init_name_field()
            self.init_password_field()
            self.init_platform_field()
            self.init_server_field()
            self.init_check_disclaimer()
            self.init_check_save()
            self.init_check_auto()

        self.init_disclaimer_link()
        self.layout.setColumnStretch(0, 0)
        self.layout.setColumnStretch(1, 1)
        self.layout.setColumnStretch(2, 1)
        user_w, user_h = get_user_resolution()
        self.init_login_button(user_h)
        self.resize(int(0.26 * user_w), int(0.12 * user_h))
        self.setStyleSheet(wgr_data.get_color_scheme())
        self.setWindowTitle(f'Warship Girls Viewer v{get_app_version()} Login')

    def init_name_field(self, text: str = ''):
        label_name = create_label('Username')
        self.lineEdit_username.setClearButtonEnabled(True)

        if text == '':
            self.lineEdit_username.setPlaceholderText('Please enter your username')
        else:
            self.lineEdit_username.setText(text)

        self.layout.addWidget(label_name, 0, 0)
        self.layout.addWidget(self.lineEdit_username, 0, 1, 1, 2)

    def init_password_field(self, text: str = ''):
        label_password = create_label('Password')
        self.lineEdit_password.setClearButtonEnabled(True)
        self.lineEdit_password.setEchoMode(QLineEdit.Password)

        if text == '':
            self.lineEdit_password.setPlaceholderText('Please enter your password')
        else:
            self.lineEdit_password.setText(text)

        self.layout.addWidget(label_password, 1, 0)
        self.layout.addWidget(self.lineEdit_password, 1, 1, 1, 2)

    def init_platform_field(self, text: str = ''):
        label_platform = create_label('Platform')
        # platforms = ["Choose your platform", "CN-iOS", "CN-Android", "International", "JP"]
        platforms = ["Choose your platform", "CN-iOS", "CN-Android"]
        self.combo_platform.addItems(platforms)
        self.combo_platform.currentTextChanged.connect(self.update_server_box)

        if text == '':
            pass
        else:
            self.combo_platform.setCurrentText(text)

        self.layout.addWidget(label_platform, 2, 0)
        self.layout.addWidget(self.combo_platform, 2, 1, 1, 2)

    def init_server_field(self, text: str = ''):
        label_server = create_label('Server')
        self.combo_server.currentTextChanged.connect(self.update_server)

        if text == '':
            pass
        else:
            self.combo_server.setCurrentText(text)

        self.layout.addWidget(label_server, 3, 0)
        self.layout.addWidget(self.combo_server, 3, 1, 1, 2)

    def init_check_disclaimer(self, checked: bool = False):
        self.check_disclaimer.setChecked(checked)
        self.check_disclaimer.stateChanged.connect(self.on_disclaimer_clicked)
        self.layout.addWidget(self.check_disclaimer, 4, 1)

    def init_disclaimer_link(self):
        label = QLabel()
        disclaimer = '<a href=\"{}\"> Terms and Conditions </a>'.format('TODO')
        label.setText(f'{disclaimer}')
        label.linkActivated.connect(open_disclaimer)
        self.layout.addWidget(label, 4, 2)

    def init_check_save(self, checked: bool = False):
        self.check_save.setChecked(checked)
        self.check_save.stateChanged.connect(self.on_save_clicked)
        self.layout.addWidget(self.check_save, 5, 1, 1, 2)

    def init_check_auto(self, checked: bool = False):
        self.check_auto.setChecked(checked)
        self.check_auto.stateChanged.connect(self.on_auto_clicked)
        self.layout.addWidget(self.check_auto, 6, 1, 1, 2)

    def init_login_button(self, user_h: int):
        self.login_button.clicked.connect(self.start_login)
        # set an empty gap row
        self.layout.addWidget(self.login_button, 8, 0, 1, 3)
        self.layout.setRowMinimumHeight(7, int(0.03 * user_h))

    # ================================
    # General
    # ================================

    def login_success(self):
        self.mi.show()
        self.close()

    def login_failed(self):
        self.login_button.setText('Login')
        self.login_button.setEnabled(True)
        self.check_auto.setText('Auto login on the application start')
        self.container.setEnabled(True)

    def wait_five_seconds(self):
        # It's ugly, but it works. QThread approach won't work
        count = 0
        while True:
            # logging.debug(count)
            time.sleep(0.01)
            if count == 500:
                break
            elif self.check_auto.isChecked() is False:
                raise InterruptExecution()
            else:
                count += 1
        logging.info('LOGIN - Starting auto login')
        self.sig_login.emit()

    def _get_password(self) -> str:
        if wgr_data.is_key_exists(self.key_filename) and self.qsettings.contains('Login/password'):
            try:
                key = self.encryptor.load_key(wgr_data.get_key_path(self.key_filename))
                res = self.encryptor.decrypt_data(key, self.qsettings.value('Login/password')).decode("utf-8")
            except AttributeError:
                res = ''
                popup_msg('Error: Key file or config file may be corrupted.')
                # TODO: reset them
        else:
            res = ''
        return res

    # ================================
    # Events
    # ================================

    def on_disclaimer_clicked(self):
        self.qsettings.setValue('Login/disclaimer', self.check_disclaimer.isChecked())

    def on_save_clicked(self):
        if self.check_save.isChecked():
            self.qsettings.beginGroup('Login')
            self.qsettings.setValue("save", self.check_save.isChecked())
            self.qsettings.setValue("server_text", self.combo_server.currentText())
            self.qsettings.setValue("platform_text", self.combo_platform.currentText())
            self.qsettings.setValue("username", self.lineEdit_username.text())
            self.qsettings.setValue("password", self._get_password())
            self.qsettings.setValue("disclaimer", self.check_disclaimer.isChecked())
            self.qsettings.endGroup()
        else:
            self.qsettings.remove("Login")
            wgr_data.del_key_file(self.key_filename)

    def on_auto_clicked(self):
        if self.check_auto.isChecked():
            # off -> on
            self.check_auto.setText('Will auto login on next start up')
        else:
            self.check_auto.setText('Auto login on the application start')
            self.login_button.setEnabled(True)
        self.qsettings.setValue("Login/auto", self.check_auto.isChecked())

    def update_server_box(self, text: str):
        self.combo_server.clear()
        if text == "CN-iOS":
            servers = ["列克星敦", "维内托"]
            self.channel = "100020"
        elif text == "CN-Android":
            servers = ["胡德", "俾斯麦", "昆西", "长春"]
            self.channel = "100015"
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

    def update_server(self, text: str):
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
            logging.error(f"Invalid server name: {text}")

    @pyqtSlot()
    def start_login(self):
        if self.check_disclaimer.isChecked() is True:
            self.container.setEnabled(False)
            self.on_save_clicked()
            self._check_password()
        else:
            popup_msg('Read disclaimer and check to proceed')

    def handle_result1(self, result: bool):
        logging.debug(f'LOGIN - First fetch result {result}')
        self.res1 = result
        if self.res1 is True:
            self.bee2.start()
        else:
            self.login_failed()

    def handle_result2(self, result: bool):
        logging.debug(f'LOGIN - Second fetch result {result}')
        self.res2 = result

        if self.res1 == True and self.res2 == True:
            self.login_button.setText('Loading and Initializing... (rendering time varies with dock size)')
            logging.info("LOGIN - SUCCESS!")
            if self.check_auto.isChecked() is True:
                pass
            else:
                popup_msg('Login Success')
            self.mi = MainInterface(self.account.get_cookies())
            self.login_success()
        else:
            self.login_failed()
            popup_msg("Login Failed (3): Probably due to bad server connection")

    def first_fetch(self, login_account: GameLogin, username: str, password: str) -> bool:
        try:
            res1 = login_account.first_login(username, password)
        except WarshipGirlsExceptions as e:
            # TODO: May crash; cannot test w/o own simulation; need to wait next maintenance
            logging.error(f"LOGIN - {e}")
            self.login_failed()
            popup_msg(f"{e}")
            return False
        except (KeyError, requests.exceptions.ReadTimeout, AttributeError) as e:
            logging.error(f"LOGIN - {e}")
            self.login_failed()
            popup_msg("Login Failed (1): Wrong authentication information")
            return False
        return res1

    def second_fetch(self, login_account: GameLogin, server: str) -> bool:
        try:
            res2 = login_account.second_login(server)
        except (KeyError, requests.exceptions.ReadTimeout, AttributeError) as e:
            logging.error(f"LOGIN - {e}")
            self.login_failed()
            popup_msg("Login Failed (2): Probably due to bad server connection")
            return False
        return res2

    def _check_password(self):
        sess = GameSession()
        self.account = GameLogin(constants.version, self.channel, sess, self.login_button)
        _username = self.lineEdit_username.text()
        _password = self.lineEdit_password.text()

        if not wgr_data.is_key_exists(self.key_filename):
            key = self.encryptor.gen_key()
            self.encryptor.save_key(key, wgr_data.get_key_path(self.key_filename))
        else:
            key = self.encryptor.load_key(wgr_data.get_key_path(self.key_filename))
        self.qsettings.setValue('Login/password', self.encryptor.encrypt_str(key, _password))

        self.bee1 = CallbackWorker(self.first_fetch, (self.account, _username, _password), self.handle_result1)
        self.bee1.terminate()
        self.bee2 = CallbackWorker(self.second_fetch, (self.account, self.server), self.handle_result2)
        self.bee2.terminate()

        self.bee1.start()

# End of File
