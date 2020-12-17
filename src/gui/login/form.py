import logging
from typing import Tuple

import requests
import threading
import time

from PyQt5.QtCore import QSettings, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import (
    QPushButton, QLabel, QLineEdit, QComboBox, QCheckBox, QWidget,
    QGridLayout, QVBoxLayout
)

from src import data as wgv_data
from src import utils as wgv_utils
from src.func import qsettings_keys as QKEYS
from src.exceptions.custom import InterruptExecution
from src.exceptions.wgr_error import WarshipGirlsExceptions
from src.func.encryptor import Encryptor
from src.func.worker import CallbackWorker
from src.gui.main_interface import MainInterface
from .game_login import GameLogin
from .session import LoginSession
from .version_check import WGViewerVersionCheck


def create_label(text: str) -> QLabel:
    _str = '<font size="4"> ' + text + ' </font>'
    _res = QLabel(_str)
    return _res


class LoginForm(QWidget):
    sig_login = pyqtSignal()
    # TODO: get a logger with LOGIN, and replace all of them in login module
    def __init__(self):
        super().__init__()
        WGViewerVersionCheck(self)

        self.sig_login.connect(self.start_login)
        self.qsettings = QSettings(wgv_data.get_qsettings_file(), QSettings.IniFormat)
        self.encryptor = Encryptor()
        self.channel = ""
        self.server = ""
        self.mi = None
        self.res1: bool = False
        self.res2: bool = False

        self.lineEdit_username = QLineEdit()
        self.lineEdit_password = QLineEdit()
        self.combo_platform = QComboBox()
        self.combo_server = QComboBox()
        # TODO? it's hard to get this checkbox to render the same way across platforms (even with get_user_resolution())
        self.check_disclaimer = QCheckBox('I have read')
        # TODO? trailing space
        # To limit the trailing space of the checkbox text with max width; still, there is ~2 whitespaces width space presents
        # set text all in label would cause user unable to click text to toggle checkbox; differs from other checkbox, (bad design IMO)
        user_w, _ = wgv_utils.get_user_resolution()
        self.check_disclaimer.setMaximumWidth(int(0.08 * user_w))
        self.check_save = QCheckBox("Store login info locally with encryption")
        self.check_auto = QCheckBox("Auto login on the application start")
        self.button_login = QPushButton("Login")
        self.button_bypass = QPushButton("Bypass Login with Existing Cookie")
        self.button_bypass.setToolTip(
            "If you previously logged in with WGViewer AND haven't logged in through other means,\n"
            "you may use this option to bypass login.")

        self.container = QWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.container)
        self.layout = QGridLayout(self.container)

        self.init_ui()
        self.setLayout(main_layout)

        self.auto_start()

    def auto_start(self) -> None:
        if self.qsettings.value(QKEYS.LOGIN_AUTO, type=bool) is True:
            # QThread cannot handle exceptions for this one
            try:
                # In case user manually log-in
                self.button_login.setEnabled(False)
                self.button_bypass.setEnabled(False)
                self.check_auto.setText('!! Login auto starts in 5 seconds. Uncheck to pause !!')
                threading.Thread(target=self.wait_five_seconds).start()
            except InterruptExecution:
                pass
        else:
            pass

    # ================================
    # Initialization
    # ================================

    def init_ui(self) -> None:
        if self.qsettings.value(QKEYS.LOGIN_SAVE, type=bool) is True:
            name = self.qsettings.value(QKEYS.LOGIN_USER)
            server = self.qsettings.value(QKEYS.LOGIN_SERVER)
            platform = self.qsettings.value(QKEYS.LOGIN_PLATFORM)
            disclaimer = self.qsettings.value(QKEYS.LOGIN_DISCLAIMER, type=bool)
            auto_login = self.qsettings.value(QKEYS.LOGIN_AUTO, type=bool)

            # Don't change the order
            self.init_name_field(name)
            self.init_password_field(self._get_password())
            self.init_server_field(server)
            self.init_platform_field(platform)
            if disclaimer is True:
                self.init_check_disclaimer(True)
            else:
                self.init_check_disclaimer(False)
            self.init_check_save(True)
            if auto_login is True:
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
        user_w, user_h = wgv_utils.get_user_resolution()
        self.init_login_buttons(user_h)
        self.resize(int(0.26 * user_w), int(0.12 * user_h))
        self.setStyleSheet(wgv_utils.get_color_scheme())
        self.setWindowTitle(f'Warship Girls Viewer v{wgv_utils.get_app_version()} Login')

    def init_name_field(self, text: str = '') -> None:
        label_name = create_label('Username')
        self.lineEdit_username.setClearButtonEnabled(True)

        if text == '':
            self.lineEdit_username.setPlaceholderText('Please enter your username')
        else:
            self.lineEdit_username.setText(text)

        self.layout.addWidget(label_name, 0, 0)
        self.layout.addWidget(self.lineEdit_username, 0, 1, 1, 2)

    def init_password_field(self, text: str = '') -> None:
        label_password = create_label('Password')
        self.lineEdit_password.setClearButtonEnabled(True)
        self.lineEdit_password.setEchoMode(QLineEdit.Password)

        if text == '':
            self.lineEdit_password.setPlaceholderText('Please enter your password')
        else:
            self.lineEdit_password.setText(text)

        self.layout.addWidget(label_password, 1, 0)
        self.layout.addWidget(self.lineEdit_password, 1, 1, 1, 2)

    def init_platform_field(self, text: str = '') -> None:
        label_platform = create_label('Platform')
        # platforms = ["Choose your platform", "CN-iOS", "CN-Android", "International", "JP"]
        platforms = ["CN-iOS", "CN-Android"]
        self.combo_platform.setPlaceholderText('Choose your platform')
        self.combo_platform.addItems(platforms)
        self.combo_platform.currentTextChanged.connect(self.update_server_box)

        if text == '':
            pass
        else:
            self.combo_platform.setCurrentText(text)

        self.layout.addWidget(label_platform, 2, 0)
        self.layout.addWidget(self.combo_platform, 2, 1, 1, 2)

    def init_server_field(self, text: str = '') -> None:
        label_server = create_label('Server')
        self.combo_server.currentTextChanged.connect(self.update_server)

        if text == '':
            pass
        else:
            self.combo_server.setCurrentText(text)

        self.layout.addWidget(label_server, 3, 0)
        self.layout.addWidget(self.combo_server, 3, 1, 1, 2)

    def init_check_disclaimer(self, checked: bool = False) -> None:
        self.check_disclaimer.setChecked(checked)
        self.check_disclaimer.stateChanged.connect(self.on_disclaimer_clicked)
        self.layout.addWidget(self.check_disclaimer, 4, 1)

    def init_disclaimer_link(self) -> None:
        label = QLabel()
        disclaimer = '<a href=\"{}\"> Terms and Conditions </a>'.format('TODO')
        label.setText(f'{disclaimer}')
        label.linkActivated.connect(wgv_utils.open_disclaimer)
        self.layout.addWidget(label, 4, 2)

    def init_check_save(self, checked: bool = False) -> None:
        self.check_save.setChecked(checked)
        self.check_save.stateChanged.connect(self.on_save_clicked)
        self.layout.addWidget(self.check_save, 5, 1, 1, 2)

    def init_check_auto(self, checked: bool = False) -> None:
        self.check_auto.setChecked(checked)
        self.check_auto.stateChanged.connect(self.on_auto_clicked)
        self.layout.addWidget(self.check_auto, 6, 1, 1, 2)

    def init_login_buttons(self, user_h: int) -> None:
        self.button_login.clicked.connect(self.start_login)
        self.button_bypass.clicked.connect(self.start_bypass_login)
        # set an empty gap row
        self.layout.addWidget(self.button_bypass, 8, 0, 1, 3)
        self.layout.addWidget(self.button_login, 9, 0, 1, 3)
        self.layout.setRowMinimumHeight(7, int(0.03 * user_h))

    # ================================
    # General
    # ================================

    def login_success(self, is_bypass: bool = False) -> None:
        if is_bypass is True:
            self.mi = MainInterface(wgv_data.load_cookies())
        else:
            self.mi = MainInterface(self.account.get_cookies())
        self.mi.show()
        self.close()

    def login_failed(self) -> None:
        self.button_login.setText('Login')
        self.button_login.setEnabled(True)
        self.check_auto.setText('Auto login on the application start')
        self.container.setEnabled(True)

    def wait_five_seconds(self) -> None:
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
        if wgv_data.is_key_exists() and self.qsettings.contains(QKEYS.LOGIN_PSWD):
            try:
                key = self.encryptor.load_key(wgv_data.get_key_path())
                res = self.encryptor.decrypt_data(key, self.qsettings.value(QKEYS.LOGIN_PSWD)).decode("utf-8")
            except AttributeError:
                res = ''
                wgv_utils.popup_msg('Error: Key file or config file may be corrupted.')
        else:
            res = ''
        return res

    # ================================
    # Events
    # ================================

    def on_disclaimer_clicked(self) -> None:
        self.qsettings.setValue(QKEYS.LOGIN_DISCLAIMER, self.check_disclaimer.isChecked())

    def on_save_clicked(self) -> None:
        if self.check_save.isChecked():
            self.qsettings.setValue(QKEYS.LOGIN_SAVE, self.check_save.isChecked())
            self.qsettings.setValue(QKEYS.LOGIN_SERVER, self.combo_server.currentText())
            self.qsettings.setValue(QKEYS.LOGIN_PLATFORM, self.combo_platform.currentText())
            self.qsettings.setValue(QKEYS.LOGIN_USER, self.lineEdit_username.text())
            self.qsettings.setValue(QKEYS.LOGIN_PSWD, self._get_password())
            self.qsettings.setValue(QKEYS.LOGIN_DISCLAIMER, self.check_disclaimer.isChecked())
        else:
            self.qsettings.remove(QKEYS.LOGIN)
            wgv_data.del_key_file()
            self.lineEdit_username.clear()
            self.lineEdit_password.clear()
            self.combo_platform.setCurrentText(self.combo_platform.itemText(0))
            self.combo_server.setCurrentText(self.combo_server.itemText(0))
            self.check_disclaimer.setChecked(False)
            self.check_auto.setChecked(False)

    def on_auto_clicked(self) -> None:
        if self.check_auto.isChecked():
            # off -> on
            self.check_auto.setText('Will auto login on next start up')
        else:
            self.check_auto.setText('Auto login on the application start')
            self.button_login.setEnabled(True)
            self.button_bypass.setEnabled(True)
        self.qsettings.setValue(QKEYS.LOGIN_AUTO, self.check_auto.isChecked())

    def update_server_box(self, text: str) -> None:
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

    def update_server(self, text: str) -> None:
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
    def start_login(self) -> None:
        if self.check_disclaimer.isChecked() is True:
            self.container.setEnabled(False)
            self.on_save_clicked()
            self._check_password()
        else:
            wgv_utils.popup_msg('Read disclaimer and check to proceed')

    def start_bypass_login(self) -> None:
        user_cookie = wgv_data.load_cookies()
        if 'cookies' in user_cookie and 'hf_skey' in user_cookie['cookies']:
            token = user_cookie['cookies']['hf_skey']
            if token == "" or len(token) < 50:
                # The random part is 32, the timestamp is 10, the UID part is at least 10
                res = False
            else:
                res = True
        else:
            res = False

        if res is True:
            self.login_success(True)
        else:
            self.button_bypass.setEnabled(False)
            wgv_utils.popup_msg("Your cookies is invalid. Please use Login")

    def handle_result1(self, result: Tuple[bool, str]) -> None:
        logging.debug(f'LOGIN - First fetch result {result}')
        self.res1 = result[0]
        if self.res1 is True:
            self.bee2.start()
        else:
            self.login_failed()
            err_msg = result[1] if result[1] != '' else "Unexpected Connection Error"
            wgv_utils.popup_msg(err_msg)

    def handle_result2(self, result: Tuple[bool, str]) -> None:
        logging.debug(f'LOGIN - Second fetch result {result}')
        self.res2 = result[0]

        if self.res2 is True:
            pass
        else:
            self.login_failed()
            wgv_utils.popup_msg(result[1])
            return

        if self.res1 == True and self.res2 == True:
            self.button_login.setText('Loading and Initializing... (rendering time varies with dock size)')
            logging.info("LOGIN - SUCCESS!")
            # No popup msg on Login Success
            # if self.check_auto.isChecked() is True:
            #     pass
            # else:
            #     wgv_utils.popup_msg('Login Success')
            self.login_success()
        else:
            self.login_failed()
            wgv_utils.popup_msg("Login Failed (3): Probably due to bad server connection")

    @staticmethod
    def first_fetch(login_account: GameLogin, username: str, password: str) -> Tuple[bool, str]:
        try:
            res1 = login_account.first_login(username, password)
        except WarshipGirlsExceptions as e:
            # Lesson: Handle GUI actions (e.g. popup_msg) outside the thread; otherwise, the GUI is blocked
            logging.error(f"LOGIN - {e}")
            return False, str(e)
        except (KeyError, requests.exceptions.ReadTimeout, AttributeError) as e:
            logging.error(f"LOGIN - {e}")
            msg = "Login Failed (1): Wrong authentication information"
            return False, msg
        return res1, ""

    @staticmethod
    def second_fetch(login_account: GameLogin, server: str) -> Tuple[bool, str]:
        try:
            res2 = login_account.second_login(server)
        except (KeyError, requests.exceptions.ReadTimeout, AttributeError) as e:
            logging.error(f"LOGIN - {e}")
            msg = "Login Failed (2): Probably due to bad server connection"
            return False, msg
        return res2, ""

    def _check_password(self) -> None:
        sess = LoginSession()
        self.account = GameLogin(wgv_utils.get_game_version(), self.channel, sess, self.button_login)
        _username = self.lineEdit_username.text()
        _password = self.lineEdit_password.text()

        if not wgv_data.is_key_exists():
            key = self.encryptor.gen_key()
            self.encryptor.save_key(key, wgv_data.get_key_path())
        else:
            key = self.encryptor.load_key(wgv_data.get_key_path())
        self.qsettings.setValue(QKEYS.LOGIN_PSWD, self.encryptor.encrypt_str(key, _password))

        self.bee1 = CallbackWorker(self.first_fetch, (self.account, _username, _password), self.handle_result1)
        self.bee1.terminate()
        self.bee2 = CallbackWorker(self.second_fetch, (self.account, self.server), self.handle_result2)
        self.bee2.terminate()

        self.bee1.start()

# End of File
