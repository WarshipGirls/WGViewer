import os

import re
import sys

from datetime import timedelta

from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QSize, QTimer, QSettings
from PyQt5.QtGui import QIcon, QCloseEvent, QResizeEvent
from PyQt5.QtWidgets import (
    QTableView, QAbstractItemView,
    QVBoxLayout, QHBoxLayout,
    QDockWidget, QWidget, QLabel, QLineEdit, QMessageBox, QCheckBox, QLayout
)

from src import data as wgv_data
from src import utils as wgv_utils
from src.func import qsettings_keys as QKEYS
from src.func import logger_names as QLOGS
from src.func.log_handler import get_logger
from .resource_model import ResourceTableModel
from .align_list_view import BathListView, BuildListView, DevListView, ExpListView, TaskListView
from .constants import TASK_TYPE
from .timer_helper import get_tasks_countdowns, _calc_left_time
from .constants import EXP_LABEL_L, EXP_LABEL_R

logger = get_logger(QLOGS.SIDE_DOCK)


def get_data_path(relative_path: str) -> str:
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


class SideDock(QDockWidget):
    """
    Side Dock/Panel, named "Navy Base Overview", displays all important data of the user.
        This is the first coded QWidget of WGViewer (even before LoginForm).
    """
    sig_resized = pyqtSignal()
    sig_closed = pyqtSignal()

    def __init__(self, parent, realrun: bool):
        super(SideDock, self).__init__(parent)
        self.is_realrun = realrun

        _, self.user_screen_h = wgv_utils.get_user_resolution()
        self.qsettings = QSettings(wgv_data.get_qsettings_file(), QSettings.IniFormat)

        self.equipment_names = wgv_data.get_shipEquipmnt()
        self.ship_names = wgv_data.get_processed_userShipVo()

        # index 0 for daily, 1 for weekly, 2+ for tasks/events
        self.task_counter_desc_labels = []
        self.task_counter_labels = []
        self.task_counter_timers = []
        self.task_counters = []

        self.name_layout_widget = QWidget(self)
        self.name_layout = QHBoxLayout(self.name_layout_widget)
        self.name_label = QLabel(self.name_layout_widget)
        self.lvl_label = QLabel(self.name_layout_widget)
        self.ship_count_label = QLabel(self.name_layout_widget)
        self.equip_count_label = QLabel(self.name_layout_widget)
        self.collect_count_label = QLabel(self.name_layout_widget)

        self.sign_widget = QLineEdit(self)
        self.table_model = ResourceTableModel()
        self.table_view = QTableView(self)
        self.bath_list_view = BathListView()
        self.bath_list_view_widget = QWidget(self)
        self.bath_list_view_layout = QVBoxLayout(self.bath_list_view_widget)
        self.triple_list_view_widget = QWidget(self)
        self.triple_list_view = QHBoxLayout(self.triple_list_view_widget)
        self.build_list_view = BuildListView()
        self.dev_list_view = DevListView()
        self.exp_list_view = ExpListView(parent.main_tabs)
        self.task_list_view = TaskListView()
        self.task_panel_widget = QWidget(self)
        self.task_panel_view = QHBoxLayout(self.task_panel_widget)
        self.countdowns_layout_widget = QWidget(self)
        self.countdowns_layout = QVBoxLayout(self.countdowns_layout_widget)

        self.sig_resized.connect(self.update_geometry)
        self.sig_closed.connect(parent.on_dock_closed)

        self._init_ui()
        self.set_data()

    def set_data(self) -> None:
        d = wgv_data.get_api_initGame()
        self.on_received_lists(d)
        self.on_received_resource(d)
        self.on_received_name(d)
        self.on_received_tasks(d)

    def _init_ui(self) -> None:
        self.setFloating(False)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setMinimumWidth(int(0.4 * self.user_screen_h))
        self.setWindowTitle("Navy Base Overview")

        self._init_name_info()
        self._init_sign_info()
        self._init_resource_info()
        self._init_bath_info()
        self._init_triple_list()
        self._init_task_panel()

    def _init_name_info(self) -> None:
        self.name_layout.setContentsMargins(0, 0, 0, 0)

        self.name_layout.addWidget(self.name_label)
        self.name_layout.addWidget(self.lvl_label)
        self.name_layout.addWidget(self.ship_count_label)
        self.name_layout.addWidget(self.equip_count_label)
        self.name_layout.addWidget(self.collect_count_label)

    def _init_sign_info(self) -> None:
        icon_path = get_data_path('assets/icons/sign_16.png')
        self.sign_widget.addAction(QIcon(icon_path), QLineEdit.LeadingPosition)

    def _init_resource_info(self) -> None:
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

    def _init_bath_info(self) -> None:
        self.bath_list_view_layout.setContentsMargins(0, 0, 0, 0)
        self.bath_list_view_layout.addWidget(self.bath_list_view)

    def _init_triple_list(self) -> None:
        self.triple_list_view.setContentsMargins(0, 0, 0, 0)
        self.triple_list_view.addWidget(self.build_list_view)
        self.triple_list_view.addWidget(self.dev_list_view)
        self.triple_list_view.addWidget(self.exp_list_view)

    def _init_task_panel(self) -> None:
        self.task_panel_view.setContentsMargins(0, 0, 0, 0)
        self._init_countdowns()
        self.task_panel_view.addWidget(self.task_list_view)
        self.task_panel_view.addWidget(self.countdowns_layout_widget)

    def _init_countdowns(self) -> None:
        # TODO? design problem now the most suitable count is 4, 5 would be max
        #   although MoeFantasy opens mostly 1 event at a time, rarely 2.
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

        _, _, d_counter, w_counter = get_tasks_countdowns()
        self.task_counters.append(d_counter)
        self.task_counters.append(w_counter)

        self._init_task_counters()

    # ================================
    # Getter / Setter
    # ================================

    def add_task_countdown(self, text: str, _time: int, idx: int) -> None:
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

    def get_ship_name(self, _id):
        return self.ship_names[str(_id)]['Name']

    def get_equip_name(self, cid: int) -> str:
        return next((i for i in self.equipment_names if i['cid'] == cid), {'title': '?'})['title']

    @staticmethod
    def get_ship_type(_id: int) -> str:
        return wgv_utils.get_build_type(_id)

    @staticmethod
    def _remove_widget(parent, widget: [QLayout, QWidget]) -> None:
        logger.warning("Deleting widget")
        parent.removeWidget(widget)
        widget.deleteLater()
        widget = None
        return

    def get_exp_list_view(self) -> ExpListView:
        return self.exp_list_view

    # ================================
    # Timer Related
    # ================================

    def count_down(self, counters: list, labels: list, timers: list, idx: int) -> None:
        # TODO? refactor; each list view has its own countdown method?
        counters[idx] -= 1
        if counters[idx] > 0:
            pass
        else:
            if counters == self.task_counters:
                if idx < 2:
                    # refreshing daily/weekly timers
                    _, _, d, w = get_tasks_countdowns()
                    counters[0] = d
                    counters[1] = w
                else:
                    counters[idx] = 0
                    timers[idx].stop()
                    self._remove_widget(self.countdowns_layout, labels[idx])
                    self._remove_widget(self.countdowns_layout, self.task_counter_desc_labels[idx])
                    return
            elif counters == self.bath_list_view.get_counters():
                counters[idx] = 0
                timers[idx].stop()
                self.bath_list_view.update_item(idx, 0, "Repairing Dock Unused")
                self.bath_list_view.update_item(idx, 1, "--:--:--")
            elif counters == self.exp_list_view.get_counters():
                counters[idx] = 0
                timers[idx].stop()
                # To avoid "Idling" (uninitialized) issue
                labels[idx].setText(str(timedelta(seconds=counters[idx])))
                if self.is_realrun:
                    self.exp_list_view.auto_restart(idx)
                else:
                    # otherwise will cause problem
                    pass
            else:
                counters[idx] = 0
                timers[idx].stop()
        labels[idx].setText(str(timedelta(seconds=counters[idx])))

    def start_new_timer(self, counters: list, labels: list, timers: list, idx: int) -> None:
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

    def _init_task_counters(self) -> None:
        self.start_new_timer(self.task_counters, self.task_counter_labels, self.task_counter_timers, 0)
        self.start_new_timer(self.task_counters, self.task_counter_labels, self.task_counter_timers, 1)

    def _process_timer_data(self, _data, view, func, item_id, counters, labels, timers) -> None:
        for i, v in enumerate(_data):
            if v["locked"] == 0:
                if "endTime" in v:
                    _left_time = _calc_left_time(v["endTime"])
                    counters[i] = _left_time
                    self.start_new_timer(counters, labels, timers, i)
                    val1 = func(v[item_id])
                    view.update_item(i, 0, val1)
                else:
                    view.update_item(i, 0, "Unused")
                    view.update_item(i, 1, "--:--:--")
            else:
                pass

    # ================================
    # Signals
    # ================================

    @pyqtSlot(dict)
    def on_received_resource(self, data: dict) -> None:
        if data is not None:
            def _get_item_by_id(item_id: int) -> int:
                return next((i for i in x if i["itemCid"] == item_id), {"num": 0})["num"]

            u = data["userVo"]
            x = data["packageVo"]
            self.table_model.update_fuel(u["oil"])
            self.table_model.update_ammo(u["ammo"])
            self.table_model.update_steel(u["steel"])
            self.table_model.update_bauxite(u["aluminium"])
            self.table_model.update_gold(u["gold"])
            self.table_model.update_repair(_get_item_by_id(541))
            self.table_model.update_build(_get_item_by_id(141))
            self.table_model.update_bp_construct(_get_item_by_id(241))
            self.table_model.update_bp_dev(_get_item_by_id(741))
            self.table_model.update_revive(_get_item_by_id(66641))
            self.table_model.update_DD(_get_item_by_id(10441))
            self.table_model.update_CA(_get_item_by_id(10341))
            self.table_model.update_BB(_get_item_by_id(10241))
            self.table_model.update_CV(_get_item_by_id(10141))
            self.table_model.update_SS(_get_item_by_id(10541))

            self.table_model.write_csv()

    @pyqtSlot(dict)
    def update_lvl_label(self, x: dict) -> None:
        # userLevelVo
        if x is not None:
            self.lvl_label.setText("Lv. " + str(x["level"]))
            lvl_tooltip = str(x["exp"]) + " / " + str(x["nextLevelExpNeed"])
            self.lvl_label.setToolTip(lvl_tooltip)

    @pyqtSlot(dict)
    def on_received_name(self, data: dict) -> None:
        if data is not None:
            x = data["userVo"]["detailInfo"]
            self.name_label.setText(x["username"])
            name_tooltip = "resource soft cap = " + str(data["userVo"]["resourcesTops"][0])
            self.name_label.setToolTip(name_tooltip)

            self.update_lvl_label(x)

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

    def update_one_expedition(self, data: dict) -> None:
        # Input = pveExploreVo['levels'][_idx]
        _idx = int(data['fleetId'])-5
        _exp_counters = self.exp_list_view.get_counters()
        _exp_counters[_idx] = _calc_left_time(data["endTime"])
        self.start_new_timer(_exp_counters, self.exp_list_view.get_counter_labels(), self.exp_list_view.get_counter_timers(), _idx)
        n = "Fleet #" + data["fleetId"] + "   " + data["exploreId"].replace("000", "-")
        self.exp_list_view.update_item(_idx, 0, n)

    def cancel_one_expedition(self, fleet_idx: int) -> None:
        self.exp_list_view.update_item(fleet_idx, 0, EXP_LABEL_L)
        self.exp_list_view.update_item(fleet_idx, 1, EXP_LABEL_R)
        self.exp_list_view.get_counters()[fleet_idx] = 0
        self.exp_list_view.get_counter_timers()[fleet_idx].stop()

    def update_expeditions(self, data: dict) -> None:
        if data is not None:
            p = sorted(data["levels"], key=lambda x: int(x['fleetId']), reverse=False)
            for _, val in enumerate(p):
                self.update_one_expedition(val)

    @pyqtSlot(dict)
    def on_received_lists(self, data: dict) -> None:
        if data is not None:
            self._process_timer_data(data["repairDockVo"], self.bath_list_view, self.get_ship_name, "shipId",
                                     self.bath_list_view.get_counters(), self.bath_list_view.get_counter_labels(), self.bath_list_view.get_counter_timers())

            self._process_timer_data(data["dockVo"], self.build_list_view, self.get_ship_type, "shipType",
                                     self.build_list_view.get_counters(), self.build_list_view.get_counter_labels(), self.build_list_view.get_counter_timers())

            self._process_timer_data(data["equipmentDockVo"], self.dev_list_view, self.get_equip_name, "equipmentCid",
                                     self.dev_list_view.get_counters(), self.bath_list_view.get_counter_labels(), self.dev_list_view.get_counter_timers())

            self.update_expeditions(data["pveExploreVo"])

    @pyqtSlot(dict)
    def on_received_tasks(self, data: dict) -> None:
        if data is not None:
            t = data["taskVo"]
            for i in t:
                stat = str(i["condition"][0]["finishedAmount"]) + " / " + str(i["condition"][0]["totalAmount"])
                desc = wgv_utils.clear_desc(i["desc"])
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
                prefix = TASK_TYPE[i['type']]
                title = f"{prefix}\t{i['title']}"
                self.task_list_view.add_item(title, stat, desc, lim_flag)

            m = data["marketingData"]["activeList"]
            for i in m:
                self.add_task_countdown(i["title"], i["left_time"], len(self.task_counters))

    # ================================
    # Events
    # ================================

    def resizeEvent(self, event: QResizeEvent) -> None:
        # overriding resizeEvent() method
        self.sig_resized.emit()
        return super(SideDock, self).resizeEvent(event)

    def closeEvent(self, event: QCloseEvent) -> None:
        cb = QCheckBox('show on start-up')
        if self.qsettings.contains(QKEYS.UI_SIDEDOCK) is True:
            cb.setChecked(self.qsettings.value(QKEYS.UI_SIDEDOCK, type=bool) is True)
        else:
            pass
        box = QMessageBox(QMessageBox.Question, "INFO", "Do you want to close side dock?\n(Can re-open in View menu)",
                          QMessageBox.Yes | QMessageBox.No, self)

        box.setStyleSheet(wgv_utils.get_color_scheme())
        box.setDefaultButton(QMessageBox.No)
        box.setCheckBox(cb)

        if box.exec() == QMessageBox.Yes:
            event.accept()
            self.sig_closed.emit()
        else:
            event.ignore()
        self.qsettings.setValue(QKEYS.UI_SIDEDOCK, cb.isChecked())

    def update_geometry(self) -> None:
        y = int(0.03 * self.user_screen_h)
        h = int(0.05 * self.user_screen_h)
        gap = int(0.01 * self.user_screen_h)

        self.name_layout_widget.setGeometry(0, y, self.geometry().width(), h)
        self.sign_widget.setGeometry(0, y + h, self.geometry().width(), y)

        y = int(2 * y + h + gap)
        h = int(0.09 * self.user_screen_h)
        self.table_view.setGeometry(0, y, self.geometry().width(), h)
        for i in range(5):
            self.table_view.setColumnWidth(i, self.geometry().width() / 5)
        for i in range(3):
            self.table_view.setRowHeight(i, h / 3)

        y = y + h + gap
        self.bath_list_view_widget.setGeometry(0, y, self.geometry().width(), h)

        y = y + h + gap
        self.triple_list_view_widget.setGeometry(0, y, self.geometry().width(), h)

        y = y + h + gap
        h = int(0.19 * self.user_screen_h)
        self.task_panel_widget.setGeometry(0, y, self.geometry().width(), h)

# End of File
