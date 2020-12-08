import logging
import os
import pytz
import re
import sys
import time

from datetime import datetime, timedelta

from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QSize, QTimer, QSettings
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QTableView, QAbstractItemView,
    QVBoxLayout, QHBoxLayout,
    QDockWidget, QWidget, QLabel, QLineEdit, QMessageBox, QCheckBox
)

from src import data as wgr_data
from src.func import constants as CONST
from src.func.helper import Helper
from src.utils import clear_desc, get_user_resolution
from .resource_model import ResourceTableModel
from .align_list_view import BathListView, BuildListView, DevListView, ExpListView, TaskListView


def get_data_path(relative_path):
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


class SideDock(QDockWidget):
    sig_resized = pyqtSignal()
    sig_closed = pyqtSignal()

    def __init__(self, parent):
        super(SideDock, self).__init__(parent)
        _, self.user_screen_h = get_user_resolution()
        self.qsettings = QSettings(wgr_data.get_qsettings_file(), QSettings.IniFormat)
        self.hlp = Helper()

        # index 0 for daily, 1 for weekly, 2+ for tasks/events
        self.task_counter_desc_labels = []
        self.task_counter_labels = []
        self.task_counter_timers = []
        self.task_counters = []
        self.bath_counter_labels = [None] * 4
        self.bath_counter_timers = [None] * 4
        self.bath_counters = [None] * 4
        self.build_counter_labels = [None] * 4
        self.build_counter_timers = [None] * 4
        self.build_counters = [None] * 4
        self.dev_counter_labels = [None] * 4
        self.dev_counter_timers = [None] * 4
        self.dev_counters = [None] * 4
        self.exp_counter_labels = [None] * 4
        self.exp_counter_timers = [None] * 4
        self.exp_counters = [None] * 4

        self.name_layout_widget = QWidget(self)
        self.name_layout = QHBoxLayout(self.name_layout_widget)
        self.name_label = QLabel(self.name_layout_widget)
        self.lvl_label = QLabel(self.name_layout_widget)
        self.ship_count_label = QLabel(self.name_layout_widget)
        self.equip_count_label = QLabel(self.name_layout_widget)
        self.collect_count_label = QLabel(self.name_layout_widget)

        self.sign_widget = QLineEdit(self)
        self.table_model = None
        self.table_view = None
        self.bathlist_view = None
        self.bathlist_view_widget = None
        self.bathlist_view_layout = None
        self.triple_list_view_widget = None
        self.triple_list_view = None
        self.buildlist_view = None
        self.devlist_view = None
        self.explist_view = None
        self.tasklist_view = None
        self.task_panel_view = None
        self.task_panel_widget = None
        self.countdowns_layout = None
        self.countdowns_layout_widget = None

        self.sig_resized.connect(self.update_geometry)
        self.sig_closed.connect(parent.on_dock_closed)

        self.init_ui()
        self.set_data()

    def set_data(self):
        d = wgr_data.get_api_initGame()
        self.on_received_lists(d)
        self.on_received_resource(d)
        self.on_received_name(d)
        self.on_received_tasks(d)

    def init_ui(self):
        self.setFloating(False)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setMinimumWidth(int(0.4 * self.user_screen_h))
        self.setWindowTitle("Navy Base Overview")

        self.init_name_info()
        self.init_sign_info()
        self.init_resource_info()
        self.init_bath_info()
        self.init_triple_list()
        self.init_task_panel()

    def init_name_info(self):
        self.name_layout.setContentsMargins(0, 0, 0, 0)

        self.name_layout.addWidget(self.name_label)
        self.name_layout.addWidget(self.lvl_label)
        self.name_layout.addWidget(self.ship_count_label)
        self.name_layout.addWidget(self.equip_count_label)
        self.name_layout.addWidget(self.collect_count_label)

    def init_sign_info(self):
        icon_path = get_data_path('assets/icons/sign_16.png')
        self.sign_widget.addAction(QIcon(icon_path), QLineEdit.LeadingPosition)

    def init_resource_info(self):
        data = [
            [1000000, 1000000, 1000000, 1000000, 200000],
            [10000, 10000, 10000, 10000, 100],
            [1000, 1000, 1000, 1000, 1000]
        ]
        self.table_model = ResourceTableModel(data)
        self.table_view = QTableView(self)
        self.table_view.setModel(self.table_model)
        x = 0.03 * self.user_screen_h
        self.table_view.setIconSize(QSize(x, x))
        self.table_view.verticalHeader().hide()
        self.table_view.horizontalHeader().hide()
        self.table_view.setShowGrid(False)
        self.table_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_view.setFocusPolicy(Qt.NoFocus)
        self.table_view.setSelectionMode(QAbstractItemView.NoSelection)
        self.table_view.horizontalScrollBar().setEnabled(False)
        self.table_view.verticalScrollBar().setEnabled(False)

    def init_bath_info(self):
        self.bathlist_view_widget = QWidget(self)
        self.bathlist_view_layout = QVBoxLayout(self.bathlist_view_widget)
        self.bathlist_view_layout.setContentsMargins(0, 0, 0, 0)
        self.bathlist_view = BathListView()
        for i in range(4):
            _, self.bath_counter_labels[i] = self.bathlist_view.add_item("Repairing Dock Locked", "")
        self.bathlist_view_layout.addWidget(self.bathlist_view)

    def init_triple_list(self):
        self.triple_list_view_widget = QWidget(self)
        self.triple_list_view = QHBoxLayout(self.triple_list_view_widget)
        self.triple_list_view.setContentsMargins(0, 0, 0, 0)
        self.init_construction_info()
        self.init_development_info()
        self.init_expedition_info()
        self.triple_list_view.addWidget(self.buildlist_view)
        self.triple_list_view.addWidget(self.devlist_view)
        self.triple_list_view.addWidget(self.explist_view)

    def init_construction_info(self):
        self.buildlist_view = BuildListView()
        for i in range(4):
            _, self.build_counter_labels[i] = self.buildlist_view.add_item("Constr. Slot", "Locked")

    def init_development_info(self):
        self.devlist_view = DevListView()
        for i in range(4):
            _, self.dev_counter_labels[i] = self.devlist_view.add_item("Dev. Slot", "Locked")

    def init_expedition_info(self):
        self.explist_view = ExpListView()
        for i in range(4):
            _, self.exp_counter_labels[i] = self.explist_view.add_item("Exped. Fleet", "Idling")

    def init_task_panel(self):
        self.task_panel_widget = QWidget(self)
        self.task_panel_view = QHBoxLayout(self.task_panel_widget)
        self.task_panel_view.setContentsMargins(0, 0, 0, 0)
        self.init_task_info()
        self.init_countdowns()
        self.task_panel_view.addWidget(self.tasklist_view)
        self.task_panel_view.addWidget(self.countdowns_layout_widget)

    def init_task_info(self):
        # Tasks view can be scrolled
        self.tasklist_view = TaskListView()

    def init_countdowns(self):
        # TODO? design problem now the most suitable count is 4, 5 would be max
        # although MoeFantasy opens mostly 1 event at a time, rarely 2.
        self.countdowns_layout_widget = QWidget(self)
        self.countdowns_layout = QVBoxLayout(self.countdowns_layout_widget)
        self.countdowns_layout.setContentsMargins(0, 0, 0, 0)

        l1 = QLabel(self.countdowns_layout_widget)
        l1.setToolTip("Refreshing daily at 0300 UTC+8")  # Intel' server also use CN time
        l1.setText("Next daily:")
        l1.adjustSize()
        self.task_counter_desc_labels.append(l1)

        l2 = QLabel(self.countdowns_layout_widget)
        l2.setText("Next weekly:")
        l2.setToolTip("Refreshing weekly at 0400 UTC+8 or New Year")
        l2.adjustSize()
        self.task_counter_desc_labels.append(l2)

        self.task_counter_labels.append(QLabel(self.countdowns_layout_widget))
        self.task_counter_labels.append(QLabel(self.countdowns_layout_widget))

        self.countdowns_layout.addWidget(l1)
        self.countdowns_layout.addWidget(self.task_counter_labels[0])
        self.countdowns_layout.addWidget(l2)
        self.countdowns_layout.addWidget(self.task_counter_labels[1])

        _, _, d_counter, w_counter = self.get_tasks_countdowns()
        self.task_counters.append(d_counter)
        self.task_counters.append(w_counter)

        self.init_task_counters()

    # ================================
    # Getter / Setter
    # ================================

    def add_task_countdown(self, text, _time, idx):
        l1 = QLabel(self.countdowns_layout_widget)
        l1.setText(text)
        l1.adjustSize()
        self.task_counter_desc_labels.append(l1)
        self.countdowns_layout.addWidget(l1)

        l2 = QLabel(self.countdowns_layout_widget)
        self.task_counter_labels.append(l2)
        self.task_counters.append(_time)
        self.countdowns_layout.addWidget(l2)
        self.start_new_timer(self.task_counters, self.task_counter_labels, self.task_counter_timers, idx)

    @staticmethod
    def get_tasks_countdowns():
        """
        returns [UTC+8 Time (in format), Local Time (in format), next daily (in sec), next weekly (in sec)]
        """
        utc_time = datetime.utcnow().replace(tzinfo=pytz.utc)
        cn_time = utc_time.astimezone(pytz.timezone('Asia/Shanghai'))
        local_time = utc_time.astimezone()

        def datetime_to_unixtime(t):
            return time.mktime(t.timetuple())

        if cn_time.hour < 3:
            next_daily = datetime(cn_time.year, cn_time.month, cn_time.day, 3, 0, 0, 0, tzinfo=pytz.timezone('Asia/Shanghai'))
        else:
            tmr = cn_time + timedelta(days=1)
            next_daily = datetime(tmr.year, tmr.month, tmr.day, 3, 0, 0, 0, tzinfo=pytz.timezone('Asia/Shanghai'))
        next_daily_diff = datetime_to_unixtime(next_daily) - datetime_to_unixtime(cn_time)

        if cn_time.hour < 4:
            next_weekly = datetime(cn_time.year, cn_time.month, cn_time.day, 4, 0, 0, 0, tzinfo=pytz.timezone('Asia/Shanghai'))
        else:
            next_weekly = datetime(cn_time.year, cn_time.month, cn_time.day, 4, 0, 0, 0,
                                   tzinfo=pytz.timezone('Asia/Shanghai'))
            days_diff = timedelta(days=-cn_time.weekday(), weeks=1).days
            next_weekly += timedelta(days=days_diff)
        next_year = datetime(year=cn_time.year + 1, month=1, day=1, tzinfo=pytz.timezone('Asia/Shanghai'))
        diff1 = datetime_to_unixtime(next_weekly) - datetime_to_unixtime(cn_time)
        diff2 = datetime_to_unixtime(next_year) - datetime_to_unixtime(cn_time)
        next_weekly_diff = min(diff1, diff2)
        return cn_time, local_time, next_daily_diff, next_weekly_diff

    @staticmethod
    def get_ship_name(_id):
        # TODO TODO
        return _id

    @staticmethod
    def get_equip_name(cid):
        # TODO TODO
        return cid

    @staticmethod
    def get_ship_type(_id):
        return CONST.build_type[_id]

    @staticmethod
    def _remove_widget(parent, widget):
        logging.warning("Deleting widget")
        parent.removeWidget(widget)
        widget.deleteLater()
        widget = None
        return

    # ================================
    # Timer Related
    # ================================

    def count_down(self, counters, labels, timers, idx):
        counters[idx] -= 1
        if counters[idx] > 0:
            pass
        else:
            if counters == self.task_counters:
                if idx < 2:
                    # refreshing daily/weekly timers
                    _, _, d, w = self.get_tasks_countdowns()
                    counters[0] = d
                    counters[1] = w
                else:
                    counters[idx] = 0
                    timers[idx].stop()
                    self._remove_widget(self.countdowns_layout, labels[idx])
                    self._remove_widget(self.countdowns_layout, self.task_counter_desc_labels[idx])
                    return
            elif counters == self.bath_counters:
                timers[idx].stop()
                counters[idx] = 0
                self.bathlist_view.update_item(idx, 0, "Repairing Dock Unused")
                self.bathlist_view.update_item(idx, 1, "--:--:--")
            else:
                counters[idx] = 0
                timers[idx].stop()
        labels[idx].setText(str(timedelta(seconds=counters[idx])))

    def start_new_timer(self, counters, labels, timers, idx):
        """
        Creates a QTimer() object and auto connects to 1 sec count down.
        Then auto start
        """
        tr = QTimer()
        tr.setInterval(1000)
        tr.timeout.connect(lambda: self.count_down(counters, labels, timers, idx))
        if counters == self.task_counters:
            timers.append(tr)
        else:
            timers[idx] = tr
        tr.start()

    def init_task_counters(self):
        self.start_new_timer(self.task_counters, self.task_counter_labels, self.task_counter_timers, 0)
        self.start_new_timer(self.task_counters, self.task_counter_labels, self.task_counter_timers, 1)

    # ================================
    # Signals
    # ================================

    @pyqtSlot(dict)
    def on_received_resource(self, data):
        if data is not None:
            u = data["userVo"]
            x = data["packageVo"]
            self.table_model._data[0][0] = u["oil"]
            self.table_model._data[0][1] = u["ammo"]
            self.table_model._data[0][2] = u["steel"]
            self.table_model._data[0][3] = u["aluminium"]
            self.table_model._data[0][4] = u["gold"]
            self.table_model._data[1][0] = next((i for i in x if i["itemCid"] == 541), {"num": 0})["num"]
            self.table_model._data[1][1] = next((i for i in x if i["itemCid"] == 141), {"num": 0})["num"]
            self.table_model._data[1][2] = next((i for i in x if i["itemCid"] == 241), {"num": 0})["num"]
            self.table_model._data[1][3] = next((i for i in x if i["itemCid"] == 741), {"num": 0})["num"]
            self.table_model._data[1][4] = next((i for i in x if i["itemCid"] == 66641), {"num": 0})["num"]
            self.table_model._data[2][0] = next((i for i in x if i["itemCid"] == 10441), {"num": 0})["num"]
            self.table_model._data[2][1] = next((i for i in x if i["itemCid"] == 10341), {"num": 0})["num"]
            self.table_model._data[2][2] = next((i for i in x if i["itemCid"] == 10241), {"num": 0})["num"]
            self.table_model._data[2][3] = next((i for i in x if i["itemCid"] == 10141), {"num": 0})["num"]
            self.table_model._data[2][4] = next((i for i in x if i["itemCid"] == 10541), {"num": 0})["num"]

    @pyqtSlot(dict)
    def on_received_name(self, data):
        if data is not None:
            x = data["userVo"]["detailInfo"]
            self.name_label.setText(x["username"])
            self.lvl_label.setText("Lv. " + str(x["level"]))
            lvl_tooltip = str(x["exp"]) + " / " + str(x["nextLevelExpNeed"]) + ", resource soft cap = " + str(data["userVo"]["resourcesTops"][0])
            self.lvl_label.setToolTip(lvl_tooltip)
            ship_icon = get_data_path('assets/icons/ship_16.png')
            ship_str = f"<html><img src='{ship_icon}'></html> " + str(x["shipNum"]) + " / " + str(x["shipNumTop"])
            self.ship_count_label.setText(ship_str)
            equip_icon = get_data_path('assets/icons/equip_16.png')
            equip_str = f"<html><img src='{equip_icon}'></html> " + str(x["equipmentNum"]) + " / " + str(x["equipmentNumTop"])
            self.equip_count_label.setText(equip_str)
            collect_icon = get_data_path('assets/icons/collect_16.png')
            collect_str = f"<html><img src='{collect_icon}'></html> " + str(len(data["unlockShip"])) + " / " + str(x["basicShipNum"])
            self.collect_count_label.setText(collect_str)

            self.sign_widget.setText(data["friendVo"]["sign"])

    @pyqtSlot(dict)
    def on_received_lists(self, data):
        if data is not None:
            def calc_left_time(t):
                return 0 if int(time.time()) < t else (t - int(time.time()))

            def process_data(_data, view, func, item_id, counters, labels, timers):
                for i, v in enumerate(_data):
                    if v["locked"] == 0:
                        if "endTime" in v:
                            _left_time = calc_left_time(v["endTime"])
                            counters[i] = _left_time
                            self.start_new_timer(counters, labels, timers, i)
                            val1 = func(v[item_id])
                            view.update_item(i, 0, val1)
                        else:
                            view.update_item(i, 0, "Unused")
                            view.update_item(i, 1, "--:--:--")
                    else:
                        pass

            process_data(data["repairDockVo"], self.bathlist_view, self.get_ship_name, "shipId",
                         self.bath_counters, self.bath_counter_labels, self.bath_counter_timers)

            process_data(data["dockVo"], self.buildlist_view, self.get_ship_type, "shipType",
                         self.build_counters, self.build_counter_labels, self.build_counter_timers)

            process_data(data["equipmentDockVo"], self.devlist_view, self.get_equip_name, "equipmentCid",
                         self.dev_counters, self.dev_counter_labels, self.dev_counter_timers)

            p = data["pveExploreVo"]["levels"]
            for idx, val in enumerate(p):
                left_time = calc_left_time(val["endTime"])
                self.exp_counters[idx] = left_time
                self.start_new_timer(self.exp_counters, self.exp_counter_labels, self.exp_counter_timers, idx)
                n = "Fleet #" + val["fleetId"] + "   " + val["exploreId"].replace("000", "-")
                self.explist_view.update_item(idx, 0, n)

    @pyqtSlot(dict)
    def on_received_tasks(self, data):
        if data is not None:
            t = data["taskVo"]
            for i in t:
                stat = str(i["condition"][0]["finishedAmount"]) + " / " + str(i["condition"][0]["totalAmount"])
                desc = clear_desc(i["desc"])
                if '#' in desc:
                    # TODO: (lowest priority) how to find `#s10030711#n` ? looks like not the same ID in docks
                    desc = re.sub(r'\[[^]]*\]', i["title"], desc)
                else:
                    pass
                if i['end_time'] != "":
                    desc += "\nEvent End On: " + i['end_time']
                    lim_flag = True
                else:
                    lim_flag = False
                prefix = CONST.task_type[i['type']]
                title = f"{prefix}\t{i['title']}"
                self.tasklist_view.add_item(title, stat, desc, lim_flag)

            m = data["marketingData"]["activeList"]
            for i in m:
                self.add_task_countdown(i["title"], i["left_time"], len(self.task_counters))

    @pyqtSlot(int)
    def update_fuel(self, x: int):
        self.table_model.update_fuel(x)

    # ================================
    # Events
    # ================================

    def resizeEvent(self, event):
        # overriding resizeEvent() method
        self.sig_resized.emit()
        return super(SideDock, self).resizeEvent(event)

    def closeEvent(self, event):
        cb = QCheckBox('Do not show on start-up.')
        box = QMessageBox(QMessageBox.Question, "INFO", "Do you want to close side dock?\n(Can re-open in View menu)",
                          QMessageBox.Yes | QMessageBox.No, self)

        box.setStyleSheet(wgr_data.get_color_scheme())
        box.setDefaultButton(QMessageBox.No)
        box.setCheckBox(cb)

        if box.exec() == QMessageBox.Yes:
            event.accept()
            self.sig_closed.emit()
        else:
            event.ignore()
        self.qsettings.setValue("UI/no_side_dock", cb.isChecked())

    def update_geometry(self):
        y = 0.03 * self.user_screen_h
        h = 0.05 * self.user_screen_h
        gap = 0.01 * self.user_screen_h

        self.name_layout_widget.setGeometry(0, y, self.geometry().width(), h)
        self.sign_widget.setGeometry(0, y + h, self.geometry().width(), y)

        y = 2 * y + h + gap
        h = 0.09 * self.user_screen_h
        self.table_view.setGeometry(0, y, self.geometry().width(), h)
        for i in range(5):
            self.table_view.setColumnWidth(i, self.geometry().width() / 5)
        for i in range(3):
            self.table_view.setRowHeight(i, h / 3)

        y = y + h + gap
        self.bathlist_view_widget.setGeometry(0, y, self.geometry().width(), h)

        y = y + h + gap
        self.triple_list_view_widget.setGeometry(0, y, self.geometry().width(), h)

        y = y + h + gap
        h = 0.19 * self.user_screen_h
        self.task_panel_widget.setGeometry(0, y, self.geometry().width(), h)


# End of File
