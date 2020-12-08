import ctypes
import logging
import os
import sys

from PyQt5.QtGui import QIcon, QFontDatabase
from PyQt5.QtWidgets import QApplication

from src.general import get_app_version
from src.gui.login import LoginForm


def get_data_path(relative_path: str) -> str:
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


def init_app_settings() -> None:
    WGV_APP.setWindowIcon(APP_ICON)
    app_id = u'PWYQ.WarshipGirlsViewer.WGViewer.version'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

    # This property holds the base name of the desktop entry for this application
    WGV_APP.setDesktopFileName("WGViewer")
    WGV_APP.setApplicationVersion(get_app_version())


def init_qsettings() -> None:
    WGV_APP.setOrganizationName("WarshipGirls")
    WGV_APP.setOrganizationDomain("https://github.com/WarshipGirls")
    WGV_APP.setApplicationName("Warship Girls Viewer")


def init_fonts() -> None:
    QFontDatabase().addApplicationFont(get_data_path('assets/fonts/Consolas.ttf'))


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
    logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(name)s - %(levelname)s - %(message)s')
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # running in a PyInstaller bundle
        login_form = LoginForm()
        _realrun()
    else:
        # running in a normal Python process
        assert (len(sys.argv) == 2)
        logging.info("Warship Girls Viewer started...")

        if int(sys.argv[1]):
            login_form = LoginForm()
            _realrun()
        else:
            from src.data.__auto_gen__ import start_generator
            from src.gui.main_interface import MainInterface
            from src import data as wgr_data

            assert (True == start_generator())
            mi = MainInterface(wgr_data.load_cookies(), False)
            _testrun()

    sys.exit(WGV_APP.exec_())

# End of File
