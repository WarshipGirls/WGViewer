from datetime import datetime, timedelta

import logging
import os
import pytz
import qdarkstyle
import re
import sys
import time

from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QRect, QSize, QTimer, QSettings
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTableView, QAbstractItemView
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QDockWidget, QWidget, QLabel, QLineEdit, QMessageBox, QCheckBox
from PyQt5.QtWidgets import QDesktopWidget

from .models.resource_model import ResourceTableModel
from .models.side_dock_list_view import BathListView, BuildListView, DevListView, ExpListView, TaskListView
from ..func import constants as CONST
from ..data import data as wgr_data


def get_data_path(relative_path):
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


class SideDock(QDockWidget):
    sig_resized = pyqtSignal()
    sig_closed = pyqtSignal()

    def __init__(self, parent, realrun):
        super(SideDock, self).__init__(parent)
        self.init_attr()

        self.sig_resized.connect(self.update_geometry)
        self.sig_closed.connect(parent.on_dock_closed)

        if realrun == False:
            self.test()
        else:
            self.init_ui()

    def test(self):
        self.init_ui()
        import json
        file_path = get_data_path('api_initGame.json')
        with open(file_path) as f:
            d = json.load(f)
        self.on_received_lists(d)
        self.on_received_resource(d)
        self.on_received_name(d)
        self.on_received_tasks(d)

    def init_attr(self):
        self.user_screen_h = QDesktopWidget().screenGeometry(-1).height()
        self.qsettings = QSettings(wgr_data.get_settings_file(), QSettings.IniFormat)

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

    def init_ui(self):
        self.setFloating(False)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        # TODO: after selecting a row/cell, cannot be de-selected (highlight looks ugly)
        self.setMinimumWidth(0.4 * self.user_screen_h)
        self.setWindowTitle("Navy Base Overview")

        self.init_name_info()
        self.init_sign_info()
        self.init_resource_info()
        self.init_bath_info()
        self.init_triple_list()
        self.init_task_panel()

    def init_name_info(self):
        self.name_layout_widget = QWidget(self)
        self.name_layout = QHBoxLayout(self.name_layout_widget)
        self.name_layout.setContentsMargins(0,0,0,0)
        
        self.name_label = QLabel(self.name_layout_widget)
        self.lvl_label = QLabel(self.name_layout_widget)
        self.ship_count_label = QLabel(self.name_layout_widget)
        self.equip_count_label = QLabel(self.name_layout_widget)
        self.collect_count_label = QLabel(self.name_layout_widget)

        self.name_layout.addWidget(self.name_label)
        self.name_layout.addWidget(self.lvl_label)
        self.name_layout.addWidget(self.ship_count_label)
        self.name_layout.addWidget(self.equip_count_label)
        self.name_layout.addWidget(self.collect_count_label)

    def init_sign_info(self):
        self.sign_widget = QLineEdit(self)
        icon_path = get_data_path('src/assets/icons/sign_16.png')
        self.sign_widget.addAction(QIcon(icon_path), QLineEdit.LeadingPosition);

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
        self.bathlist_view_layout.setContentsMargins(0,0,0,0)
        self.bathlist_view = BathListView(self)
        _, self.bath_counter_labels[0] = self.bathlist_view.add_item("Repairing Dock Locked", "")
        _, self.bath_counter_labels[1] = self.bathlist_view.add_item("Repairing Dock Locked", "")
        _, self.bath_counter_labels[2] = self.bathlist_view.add_item("Repairing Dock Locked", "")
        _, self.bath_counter_labels[3] = self.bathlist_view.add_item("Repairing Dock Locked", "")
        self.bathlist_view_layout.addWidget(self.bathlist_view)

    def init_triple_list(self):
        self.triple_list_view_widget = QWidget(self)
        self.triple_list_view = QHBoxLayout(self.triple_list_view_widget)
        self.triple_list_view.setContentsMargins(0,0,0,0)
        self.init_construction_info()
        self.init_development_info()
        self.init_expedition_info()
        self.triple_list_view.addWidget(self.buildlist_view)
        self.triple_list_view.addWidget(self.devlist_view)
        self.triple_list_view.addWidget(self.explist_view)

    def init_construction_info(self):
        self.buildlist_view = BuildListView(self)
        _, self.build_counter_labels[0] = self.buildlist_view.add_item("Constr. Slot", "Locked")
        _, self.build_counter_labels[1] = self.buildlist_view.add_item("Constr. Slot", "Locked")
        _, self.build_counter_labels[2] = self.buildlist_view.add_item("Constr. Slot", "Locked")
        _, self.build_counter_labels[3] = self.buildlist_view.add_item("Constr. Slot", "Locked")

    def init_development_info(self):
        self.devlist_view = DevListView(self)
        _, self.dev_counter_labels[0] = self.devlist_view.add_item("Dev. Slot", "Locked")
        _, self.dev_counter_labels[1] = self.devlist_view.add_item("Dev. Slot", "Locked")
        _, self.dev_counter_labels[2] = self.devlist_view.add_item("Dev. Slot", "Locked")
        _, self.dev_counter_labels[3] = self.devlist_view.add_item("Dev. Slot", "Locked")

    def init_expedition_info(self):
        self.explist_view = ExpListView(self)
        _, self.exp_counter_labels[0] = self.explist_view.add_item("Exped. Fleet", "Idling")
        _, self.exp_counter_labels[1] = self.explist_view.add_item("Exped. Fleet", "Idling")
        _, self.exp_counter_labels[2] = self.explist_view.add_item("Exped. Fleet", "Idling")
        _, self.exp_counter_labels[3] = self.explist_view.add_item("Exped. Fleet", "Idling")

    def init_task_panel(self):
        self.task_panel_widget = QWidget(self)
        self.task_panel_view = QHBoxLayout(self.task_panel_widget)
        self.task_panel_view.setContentsMargins(0,0,0,0)
        self.init_task_info()
        self.init_countdowns()
        self.task_panel_view.addWidget(self.tasklist_view)
        self.task_panel_view.addWidget(self.countdowns_layout_widget)

    def init_task_info(self):
        # Tasks view can be scrolled
        self.tasklist_view = TaskListView(self)

    def init_countdowns(self):
        # TODO? design problem now the most suitable count is 4, 5 would be max
        # although MoeFantasy opens mostly 1 event at a time, rarely 2.
        self.countdowns_layout_widget = QWidget(self)
        self.countdowns_layout = QVBoxLayout(self.countdowns_layout_widget)
        self.countdowns_layout.setContentsMargins(0,0,0,0)

        l1 = QLabel(self.countdowns_layout_widget)
        l1.setToolTip("Refreshing daily at 0300 UTC+8") # Intel' server also use CN time
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


    def add_task_countdown(self, text, time, idx):
        l1 = QLabel(self.countdowns_layout_widget)
        l1.setText(text)
        l1.adjustSize()
        self.task_counter_desc_labels.append(l1)
        self.countdowns_layout.addWidget(l1)

        l2 = QLabel(self.countdowns_layout_widget)
        self.task_counter_labels.append(l2)
        self.task_counters.append(time)
        self.countdowns_layout.addWidget(l2)
        self.start_new_timer(self.task_counters, self.task_counter_labels, self.task_counter_timers, idx)

    def get_tasks_countdowns(self):
        '''
        returns [UTC+8 Time (in format), Local Time (in format), next daily (in sec), next weekly (in sec)]
        '''
        utc_time = datetime.utcnow().replace(tzinfo=pytz.utc)
        cn_time = utc_time.astimezone(pytz.timezone('Asia/Shanghai'))
        local_time = utc_time.astimezone()
        def datetime_to_unixtime(t):
            return time.mktime(t.timetuple())

        next_daily = None
        if cn_time.hour < 3:
            next_daily = datetime(cn_time.year, cn_time.month, cn_time.day, 3, 0, 0, 0, tzinfo=pytz.timezone('Asia/Shanghai'))
        else:
            tmr = cn_time + timedelta(days=1)
            next_daily = datetime(tmr.year, tmr.month, tmr.day, 3, 0, 0, 0, tzinfo=pytz.timezone('Asia/Shanghai'))
        next_daily_diff = datetime_to_unixtime(next_daily) - datetime_to_unixtime(cn_time)

        next_weekly = None
        if cn_time.hour < 4:
            next_weekly = next_weekly = datetime(cn_time.year, cn_time.month, cn_time.day, 4, 0, 0, 0, tzinfo=pytz.timezone('Asia/Shanghai'))
        else:
            next_weekly = datetime(cn_time.year, cn_time.month, cn_time.day, 4, 0, 0, 0, tzinfo=pytz.timezone('Asia/Shanghai'))
            days_diff = timedelta(days=-cn_time.weekday(), weeks=1).days
            next_weekly += timedelta(days=days_diff)
        next_year = datetime(year=cn_time.year+1, month=1, day=1, tzinfo=pytz.timezone('Asia/Shanghai'))
        diff1 = datetime_to_unixtime(next_weekly) - datetime_to_unixtime(cn_time)
        diff2 = datetime_to_unixtime(next_year) - datetime_to_unixtime(cn_time)
        next_weekly_diff = min(diff1, diff2)
        return cn_time, local_time, next_daily_diff, next_weekly_diff

    def get_ship_name(self, _id):
        # TODO TODO
        return _id

    def get_equip_name(self, cid):
        # TODO TODO
        return cid

    def get_ship_type(self, _id):
        return CONST.build_type[_id]

    def _remove_widget(self, parent, widget):
        logging.warn("Deleting widget")
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
        '''
        Creates a QTimer() object and auto connects to 1 sec count down.
        Then auto start
        '''
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
        if data != None:
            u = data["userVo"]
            x = data["packageVo"]
            self.table_model._data[0][0] = u["oil"]
            self.table_model._data[0][1] = u["ammo"]
            self.table_model._data[0][2] = u["steel"]
            self.table_model._data[0][3] = u["aluminium"]
            self.table_model._data[0][4] = u["gold"]
            self.table_model._data[1][0] = next((i for i in x if i["itemCid"] == 541),{"num":0})["num"]
            self.table_model._data[1][1] = next((i for i in x if i["itemCid"] == 141),{"num":0})["num"]
            self.table_model._data[1][2] = next((i for i in x if i["itemCid"] == 241),{"num":0})["num"]
            self.table_model._data[1][3] = next((i for i in x if i["itemCid"] == 741),{"num":0})["num"]
            self.table_model._data[1][4] = next((i for i in x if i["itemCid"] == 66641),{"num":0})["num"]
            self.table_model._data[2][0] = next((i for i in x if i["itemCid"] == 10441),{"num":0})["num"]
            self.table_model._data[2][1] = next((i for i in x if i["itemCid"] == 10341),{"num":0})["num"]
            self.table_model._data[2][2] = next((i for i in x if i["itemCid"] == 10241),{"num":0})["num"]
            self.table_model._data[2][3] = next((i for i in x if i["itemCid"] == 10141),{"num":0})["num"]
            self.table_model._data[2][4] = next((i for i in x if i["itemCid"] == 10541),{"num":0})["num"]
            # formatting numbers
            for r in range(3):
                for c in range(5):
                    self.table_model._data[r][c] = f'{self.table_model._data[r][c]:,}' 

    @pyqtSlot(dict)
    def on_received_name(self, data):
        if data != None:
            x = data["userVo"]["detailInfo"]
            self.name_label.setText(x["username"])
            self.lvl_label.setText("Lv. " + str(x["level"]))
            lvl_tooltip = str(x["exp"]) + " / " + str(x["nextLevelExpNeed"]) + \
                            ", resource soft cap = " + str(data["userVo"]["resourcesTops"][0])
            self.lvl_label.setToolTip(lvl_tooltip)
            ship_icon = get_data_path('src/assets/icons/ship_16.png')
            ship_str = "<html><img src='{}'></html> ".format(ship_icon) + str(x["shipNum"]) \
                         + " / "  + str(x["shipNumTop"])
            self.ship_count_label.setText(ship_str)
            equip_icon = get_data_path('src/assets/icons/equip_16.png')
            equip_str = "<html><img src='{}'></html> ".format(equip_icon) + str(x["equipmentNum"]) \
                        + " / "  + str(x["equipmentNumTop"])
            self.equip_count_label.setText(equip_str)
            collect_icon = get_data_path('src/assets/icons/collect_16.png')
            collect_str = "<html><img src='{}'></html> ".format(collect_icon) + str(len(data["unlockShip"])) \
                        + " / " + str(x["basicShipNum"])
            self.collect_count_label.setText(collect_str)

            self.sign_widget.setText(data["friendVo"]["sign"])

    @pyqtSlot(dict)
    def on_received_lists(self, data):
        if data != None:
            def calc_left_time(t):
                return 0 if int(time.time()) < t else (t - int(time.time()))

            def process_data(data, view, func, item_id, counters, labels, timers):
                for idx, val in enumerate(data):
                    if val["locked"] == 0:
                        if "endTime" in val:
                            left_time = calc_left_time(val["endTime"])
                            counters[idx] = left_time
                            self.start_new_timer(counters, labels, timers, idx)
                            val1 = func(val[item_id])
                            view.update_item(idx, 0, val1)
                        else:
                            view.update_item(idx, 0, "Unused")
                            view.update_item(idx, 1, "--:--:--")
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
        if data != None:
            t = data["taskVo"]
            for i in t:
                stat = str(i["condition"][0]["finishedAmount"]) + " / " + str(i["condition"][0]["totalAmount"])
                desc = re.sub(r'\^.+?00000000', '', i["desc"])  # F**k MoeFantasy
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
                title = "{}\t{}".format(prefix, i['title']) # {:15s} works on terminal but not PyQt...
                self.tasklist_view.add_item(title, stat, desc, lim_flag)

            m = data["marketingData"]["activeList"]
            for i in m:
                self.add_task_countdown(i["title"], i["left_time"], len(self.task_counters))


    # ================================
    # Events
    # ================================


    def resizeEvent(self, event):
        # overriding resizeEvent() method
        self.sig_resized.emit()
        return super(SideDock, self).resizeEvent(event)

    def closeEvent(self, event):
        cb = QCheckBox('Do not show on start-up.')
        box = QMessageBox(QMessageBox.Question, "INFO", "Do you want to close side dock?\n(Can re-open in View menu)", QMessageBox.Yes | QMessageBox.No, self)
        box.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
        box.setDefaultButton(QMessageBox.No)
        box.setCheckBox(cb)

        if (box.exec() == QMessageBox.Yes):
            event.accept()
            self.sig_closed.emit()
        else:
            event.ignore()

        self.qsettings.setValue("UI/init_side_dock", cb.isChecked())

    def update_geometry(self):
        y = 0.03 * self.user_screen_h
        h = 0.05 * self.user_screen_h
        gap = 0.01 * self.user_screen_h

        self.name_layout_widget.setGeometry(0, y, self.geometry().width(), h)
        self.sign_widget.setGeometry(0, y+h, self.geometry().width(), y)

        y = 2*y + h + gap
        h = 0.09 * self.user_screen_h
        self.table_view.setGeometry(0, y, self.geometry().width(), h)
        for i in range(5):
            self.table_view.setColumnWidth(i, self.geometry().width()/5)
        for i in range(3):
            self.table_view.setRowHeight(i, h/3)

        y = y + h + gap
        self.bathlist_view_widget.setGeometry(0, y, self.geometry().width(), h)

        y = y + h + gap
        self.triple_list_view_widget.setGeometry(0, y, self.geometry().width(), h)

        y = y + h + gap
        h = 0.19 * self.user_screen_h
        self.task_panel_widget.setGeometry(0, y, self.geometry().width(), h)


# End of File