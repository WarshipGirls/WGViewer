import sys
import os
import ctypes
import logging

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from src.gui.login import LoginForm
from src.gui.main_interface import MainInterface


def set_icon(path):
    app.setWindowIcon(QIcon(path))
    myappid = u'mycompany.myproduct.subproduct.version' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

def get_data_path(relative_path):
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


if __name__ == '__main__':
    app = QApplication(sys.argv)
    icon_path = get_data_path('src/assets/favicon.ico')
    set_icon(icon_path)

    qss_path = get_data_path('src/assets/dark_style.qss')
    qss_file = open(qss_path).read()

    if 1:   # user run
        login_form = LoginForm(qss_file)
        login_form.show()
        login_form.raise_()
    else:   # test
        logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logging.info("WG Viewer started...")
        mi = MainInterface(qss_file, 0, 0, 0, False)
        mi.show()

    sys.exit(app.exec_())


# End of File