import logging
from time import sleep

from PyQt5.QtCore import QObject, pyqtSignal, QThread
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QTextEdit, QPushButton, QTableWidget, QMainWindow, QTableWidgetItem, QButtonGroup

import src.data as wgr_data

from .thermopylae.ship_window import ShipSelectWindow


class LogHandler(logging.Handler, QObject):
    sig_log = pyqtSignal(str)

    def __init__(self):
        logging.Handler.__init__(self)
        QObject.__init__(self)

    def emit(self, log_record):
        msg = str(log_record.getMessage())
        self.sig_log.emit(msg)


class Worker(QThread):
    def __init__(self, func, args):
        super(Worker, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.func(*self.args)


class TabThermopylae(QWidget):
    def __init__(self):
        super().__init__()
        self.fleets = [None] * 6

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()

        self.button1 = QPushButton('start')
        self.button2 = QPushButton('test 2')
        self.button1.clicked.connect(self.button1_on_click)
        self.button2.clicked.connect(self.button2_func)

        self.left_layout.addWidget(self.button1)
        self.left_layout.addWidget(self.button2)

        text_box = QTextEdit()
        text_box.setReadOnly(True)
        self.right_layout.addWidget(text_box)
        self.bee = Worker(self.test_process, ())
        self.bee.finished.connect(self.process_finished)
        self.bee.terminate()
        self.logger = logging.getLogger('TabThermopylae')
        log_handler = LogHandler()
        log_handler.sig_log.connect(text_box.append)
        self.logger.addHandler(log_handler)

        main_layout.addLayout(self.left_layout)
        main_layout.addLayout(self.right_layout)
        main_layout.setStretch(0, 1)
        main_layout.setStretch(1, 1)
        self.setLayout(main_layout)

        self.add_ship()

    def add_ship(self):
        self.button_group = QButtonGroup()
        # for ship_id in self.fleets:
        for i in range(len(self.fleets)):
            t = self.fleets[i]
            l = QPushButton()
            if t is None:
                l.setText('+')
            else:
                l.setText(str(t))
            l.clicked.connect(lambda _, _i=i: self.popup_select_window(_i))
            self.button_group.addButton(l)
            self.left_layout.addWidget(l)

    def handle_selection(self, ship_info: list, button_id: int):
        b = self.button_group.buttons()[button_id]
        ship_type = ship_info[0]
        ship_id = ship_info[1]
        ship_name = ship_info[2]
        ship_lvl = ship_info[3]
        if int(ship_id) in self.fleets:
            b.setText('! SHIP ALREADY EXISTS IN FLEET !')
        else:
            self.fleets[button_id] = int(ship_id)
            s = ", ".join(ship_info)
            b.setText(s)

    def popup_select_window(self, btn_id):
        self.w = ShipSelectWindow(self, btn_id)
        self.w.show()

    def button1_on_click(self):
        self.button1.setEnabled(False)
        self.bee.start()

    def test_process(self):
        # button 1 linked
        self.logger.info('starting')
        for i in range(10):
            self.logger.info(i)
            sleep(1)

    def button2_func(self):
        self.logger.info('this is button 2')

    def process_finished(self):
        self.logger.info('task is done')
        self.button1.setEnabled(True)

# End of File
