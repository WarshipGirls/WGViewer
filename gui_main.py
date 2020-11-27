import ctypes
import logging
import os
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon, QFontDatabase

from src.gui.login import LoginForm
from src.gui.main_interface import MainInterface


def get_data_path(relative_path):
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res

def set_app_icon():
    app.setWindowIcon(QIcon(get_data_path('src/assets/favicon.ico')))
    myappid = u'mycompany.myproduct.subproduct.version' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

def init_QSettings():
    app.setOrganizationName("WarshipGirls")
    app.setOrganizationDomain("https://github.com/WarshipGirls")
    app.setApplicationName("Warship Girls Viewer")

def init_fonts():
    QFontDatabase().addApplicationFont(get_data_path('src/assets/fonts/Consolas.ttf'))


if __name__ == '__main__':
    assert(len(sys.argv) == 2)

    app = QApplication([])
    set_app_icon()
    init_QSettings()
    init_fonts()

    # python gui_main.py 0/1
    if int(sys.argv[1]):   # user run
        login_form = LoginForm()
        login_form.show()
        login_form.raise_()
    else:   # test
        # NOTE!! In test run, api call to server won't work
        logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logging.info("Warship Girls Viewer started...")
        mi = MainInterface("0", "0", "0", False)
        mi.show()

    sys.exit(app.exec_())


# End of File