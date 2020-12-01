import ctypes
import logging
import os
import sys

from PyQt5.QtGui import QIcon, QFontDatabase
from PyQt5.QtWidgets import QApplication

from src.gui.login import LoginForm


def get_data_path(relative_path):
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


def set_app_icon():
    app.setWindowIcon(QIcon(get_data_path('assets/favicon.ico')))
    app_id = u'PWYQ.WarshipGirlsViewer.WGViewer.version'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)


def init_qsettings():
    app.setOrganizationName("WarshipGirls")
    app.setOrganizationDomain("https://github.com/WarshipGirls")
    app.setApplicationName("Warship Girls Viewer")


def init_fonts():
    QFontDatabase().addApplicationFont(get_data_path('assets/fonts/Consolas.ttf'))


def _realrun():
    login_form.show()
    login_form.raise_()


def _testrun():
    dev_warning = "\n\n==== TEST WARNING ====\n"
    dev_warning += "In test run, api calls to server won't work!\n"
    dev_warning += "In order to test offline, one real run (to get server data sample) is required!\n"
    dev_warning += "==== WARNING  END ====\n"
    logging.warning(dev_warning)
    mi.show()


if __name__ == '__main__':

    app = QApplication([])
    set_app_icon()
    init_qsettings()
    init_fonts()

    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # running in a PyInstaller bundle
        login_form = LoginForm()
        _realrun()
    else:
        # running in a normal Python process
        assert (len(sys.argv) == 2)
        logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logging.info("Warship Girls Viewer started...")

        if int(sys.argv[1]):
            login_form = LoginForm()
            _realrun()
        else:
            from src.gui.main_interface import MainInterface
            from src import data as wgr_data
            mi = MainInterface(wgr_data.load_cookies(), False)
            _testrun()

    sys.exit(app.exec_())

# End of File
