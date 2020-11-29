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
    myappid = u'PWYQ.WarshipGirlsViewer.WGViewer.version'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


def init_QSettings():
    app.setOrganizationName("WarshipGirls")
    app.setOrganizationDomain("https://github.com/WarshipGirls")
    app.setApplicationName("Warship Girls Viewer")


def init_fonts():
    QFontDatabase().addApplicationFont(get_data_path('assets/fonts/Consolas.ttf'))


def init_data_imports():
    assert (True == start_generator())


if __name__ == '__main__':
    assert (len(sys.argv) == 2)
    # Comment out following when using pyinstaller
    logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logging.info("Warship Girls Viewer started...")
    app = QApplication([])
    set_app_icon()
    init_QSettings()
    init_fonts()
    init_data_imports()

    # python gui_main.py 0  # test run
    # python gui_main.py 1  # real run
    if int(sys.argv[1]):
        login_form = LoginForm()
        login_form.show()
        login_form.raise_()
    else:
        dev_warning = "\n\n==== TEST WARNING ====\n"
        dev_warning += "In test run, api calls to server won't work!\n"
        dev_warning += "In order to test offline, one real run (to get server data sample) is required!\n"
        dev_warning += "==== WARNING  END ====\n"
        logging.warning(dev_warning)

        from src.gui.main_interface import MainInterface

        mi = MainInterface("0", "0", "0", False)
        mi.show()

    sys.exit(app.exec_())

# End of File
