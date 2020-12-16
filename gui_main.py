#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import ctypes
import logging
import os
import sys

from PyQt5.QtGui import QIcon, QFontDatabase
from PyQt5.QtWidgets import QApplication

from src.data import get_log_dir
from src.utils import get_app_version, get_today
from src.gui.login.form import LoginForm



def get_data_path(relative_path: str) -> str:
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


def check_py_ver() -> None:
    version = sys.version_info[0:3]
    if version < (3, 6, 0):
        sys.exit('WGViewer requires Python >= 3.6.0; your version of Python is ' + sys.version)
    else:
        pass


def init_app_settings() -> None:
    WGV_APP.setWindowIcon(APP_ICON)
    if sys.platform.startswith('win32'):
        app_id = u'PWYQ.WarshipGirlsViewer.WGViewer.version'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    else:
        pass

    # This property holds the base name of the desktop entry for this application
    WGV_APP.setDesktopFileName("WGViewer")
    WGV_APP.setApplicationVersion(get_app_version())


def init_fonts() -> None:
    QFontDatabase().addApplicationFont(get_data_path('assets/fonts/Consolas.ttf'))


def init_logging() -> None:
    _level = logging.DEBUG
    _format = ' %(asctime)s - %(name)s - %(levelname)s - %(message)s'
    _log_filename = f'wgviewer-{get_today()}.log'
    _log_filepath = get_data_path(os.path.join(get_log_dir(), _log_filename))
    _handlers = [logging.FileHandler(filename=_log_filepath, encoding='utf-8'), logging.StreamHandler()]
    logging.basicConfig(level=_level, format=_format, handlers=_handlers)


def init_qsettings() -> None:
    WGV_APP.setOrganizationName("WarshipGirls")
    WGV_APP.setOrganizationDomain("https://github.com/WarshipGirls")
    WGV_APP.setApplicationName("Warship Girls Viewer")


def _realrun() -> None:
    login_form.show()
    login_form.raise_()


def _testrun() -> None:

    dev_warning = "\n\n==== TEST WARNING ====\n"
    dev_warning += "In test run, api calls to server won't work!\n"
    dev_warning += "In order to test offline, one real run (to get server data sample) is required!\n"
    dev_warning += "==== WARNING  END ====\n"
    logging.warning(dev_warning)
    mi.show()


# ================================
# Entry Point
# ================================


if __name__ == '__main__':

    WGV_APP = QApplication([])
    APP_ICON = QIcon(get_data_path('assets/favicon.ico'))

    init_app_settings()
    init_qsettings()
    init_fonts()
    # https://stackoverflow.com/q/43109355/14561914
    init_logging()

    logging.debug(f"\nWGViewer {get_app_version()} STARTS\n")
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # running in a PyInstaller bundle
        login_form = LoginForm()
        _realrun()
    else:
        # running in a normal Python process
        check_py_ver()
        assert (len(sys.argv) == 2)

        if int(sys.argv[1]):
            login_form = LoginForm()
            _realrun()
        else:
            from src.data.__auto_gen__ import start_data_generator
            from src.utils.__auto_gen__ import start_utils_generator
            from src.gui.main_interface import MainInterface
            from src import data as wgr_data

            assert (True == start_data_generator())
            assert (True == start_utils_generator())
            mi = MainInterface(wgr_data.load_cookies(), False)
            _testrun()

    sys.exit(WGV_APP.exec_())

# End of File
