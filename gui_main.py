import ctypes
import logging
import os
import sys

from PyQt5.QtGui import QIcon, QFontDatabase
from PyQt5.QtWidgets import QApplication

from src.data.__auto_gen__ import start_generator
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
    login_form = LoginForm()
    login_form.show()
    login_form.raise_()


def _testrun():
    assert (True == start_generator())
    dev_warning = "\n\n==== TEST WARNING ====\n"
    dev_warning += "In test run, api calls to server won't work!\n"
    dev_warning += "In order to test offline, one real run (to get server data sample) is required!\n"
    dev_warning += "==== WARNING  END ====\n"
    logging.warning(dev_warning)

    from src.gui.main_interface import MainInterface
    from src import data as wgr_data

    mi = MainInterface(wgr_data.load_cookies(), False)
    mi.show()


if __name__ == '__main__':
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # !! Comment out following when using pyinstaller !!
    # !! and set if-expression to 1   (i.e. _realrun) !!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    assert (len(sys.argv) == 2)
    logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logging.info("Warship Girls Viewer started...")
    app = QApplication([])
    set_app_icon()
    init_qsettings()
    init_fonts()

    # python gui_main.py 0  # test run
    # python gui_main.py 1  # real run
    if int(sys.argv[1]):
        _realrun()
    else:
        _testrun()

    sys.exit(app.exec_())

# End of File
