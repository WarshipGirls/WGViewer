from typing import Tuple, Callable, List, Union

from PyQt5.QtCore import Qt, QTimer, QModelIndex
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor
from PyQt5.QtWidgets import QTreeView, QAbstractItemView, QHeaderView, QWidget

from src.data import load_cookies
from src.exceptions.wgr_error import get_error, WarshipGirlsExceptions
from src.func import logger_names as QLOGS
from src.func.log_handler import get_new_logger
from src import utils as wgv_utils
from src.wgr import API_EXPLORE
from . import constants as CONST


class AlignListView(QTreeView):
    """
    Custom View for aligning left and right items
    """

    def __init__(self):
        # Lesson: PUT keyword argument between *args and **kwargs!! e.g. __init__(self, *args, rows=None, **kwargs)
        super().__init__()
        self.logger = get_new_logger(name=QLOGS.SIDE_DOCK, level=QLOGS.LVL_INFO, signal=None)

        self.init_ui()

        self.counter_labels = [None] * 4
        self.counter_timers = [None] * 4  # QTimer
        self.counters = [None] * 4  # seconds left

    # ================================
    # Getter / Setter
    # ================================

    def get_counter_labels(self) -> List[Union[QStandardItem, None]]:
        return self.counter_labels

    def get_counters(self) -> List[Union[int, None]]:
        return self.counters

    def get_counter_timers(self) -> List[Union[QTimer, None]]:
        return self.counter_timers

    # ================================
    # UI
    # ================================

    def init_ui(self) -> None:
        self.setModel(QStandardItemModel(self))
        self.model().setColumnCount(2)
        self.setRootIsDecorated(False)
        self.setHeaderHidden(True)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setFocusPolicy(Qt.NoFocus)
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(0, QHeaderView.Stretch)
        self.header().setSectionResizeMode(1, QHeaderView.ResizeToContents)

        self.doubleClicked.connect(self.on_double_click)
        self.clicked.connect(self.on_single_click)

    def on_single_click(self, index: QModelIndex) -> None:
        pass

    def on_double_click(self, index: QModelIndex) -> None:
        pass

    def add_item(self, key: str, value: str, desc: str = None, is_limited: bool = False) -> Tuple[QStandardItem, QStandardItem]:
        # TODO: add function, when user clicked, pop up build/dev/repair etc
        first = QStandardItem(key)
        if desc is not None:
            first.setToolTip(desc)
        else:
            pass
        if is_limited:
            first.setForeground(QColor(255, 51, 51))
        else:
            pass
        second = QStandardItem(value)
        second.setTextAlignment(Qt.AlignRight)
        self.model().appendRow([first, second])
        # index = self.model().rowCount()
        # return index, first, second
        return first, second

    def update_item(self, row, col, val):
        self.model().item(row, col).setText(str(val))

    # ================================
    # Helpers
    # ================================

    def _reconnecting_calls(self, func: Callable, func_info: str) -> [dict, object]:
        # This redundancy while-loop (compared to api.py's while-loop) deals with WarshipGirlsExceptions;
        #   while the other one deals with URLError etc
        res = False  # status
        data = None
        tries = 0
        while not res:
            try:
                self.logger.debug(f"{func_info}...")
                res, data = func()
            except WarshipGirlsExceptions as e:
                self.logger.warning(f"Failed to {func_info} due to {e}. Trying reconnecting...")
                wgv_utils.set_sleep()
            tries += 1
            if tries >= self.reconnection_limit:
                break
            else:
                pass
        return data


class BathListView(AlignListView):
    def __init__(self):
        super().__init__()
        for i in range(4):
            _, self.counter_labels[i] = self.add_item(CONST.BATH_LABEL_L, CONST.BATH_LABEL_R)

    def on_single_click(self, index: QModelIndex) -> None:
        pass

    def on_double_click(self, index: QModelIndex) -> None:
        pass
        # boat/repair/{ship cid}/{slot}
        # boat/rubdown/{ship cid}


class BuildListView(AlignListView):
    def __init__(self):
        super().__init__()
        for i in range(4):
            _, self.counter_labels[i] = self.add_item(CONST.BLD_LABEL_L, CONST.BLD_LABEL_R)

    def on_single_click(self, index: QModelIndex) -> None:
        pass

    def on_double_click(self, index: QModelIndex) -> None:
        pass
        # dock/buildBoat/{slot}/{fuel}/{ammo}/{steel}/{baux}
        # dock/getBoat/{slot}


class DevListView(AlignListView):
    def __init__(self):
        super().__init__()
        for i in range(4):
            _, self.counter_labels[i] = self.add_item(CONST.DEV_LABEL_L, CONST.DEV_LABEL_R)

    def on_single_click(self, index: QModelIndex) -> None:
        pass

    def on_double_click(self, index: QModelIndex) -> None:
        pass
        # dock/buildEquipment/{slot}/{fuel}/{ammo}/{steel}/{baux}
        # dock/dismantleEquipment       # TODO: #103
        # dock/getEquipment/2/


class ExpListView(AlignListView):
    def __init__(self, main_tabs):
        super().__init__()
        self.main_tabs = main_tabs

        self.api = API_EXPLORE(load_cookies())
        self.reconnection_limit = 3
        for i in range(4):
            _, self.counter_labels[i] = self.add_item(CONST.EXP_LABEL_L, CONST.EXP_LABEL_R)

    def on_single_click(self, index: QModelIndex) -> None:
        """
        Single click simply jumps to the Tab Expedition (when the tab is open)
        @param index: QModelIndex object
        @type index: QModelIndex
        @return: None
        @rtype: None
        """
        # Changes view to Tab Expedition upon clicking
        # HARDCODING
        self.main_tabs.tabs.setCurrentWidget(self.main_tabs.tabs.findChild(QWidget, 'tab_exp'))

    def on_double_click(self, index: QModelIndex) -> None:
        """
        Double clicks serves the same function as the START/STOP button on Tab Expedition
            - If on expedition, it stops the current expedition
            - If on idle state, it collects rewards (if possible) and re-start expedition
        @param index: QModelIndex object
        @type index: QModelIndex
        @return: None
        @rtype: None
        """
        fleet_idx = index.row()
        tab_exp = self.main_tabs.tabs.findChild(QWidget, 'tab_exp')
        tab_exp.fleet_table.on_button_clicked(fleet_idx)

    def auto_restart(self, index: int) -> None:
        """
        Given the index of the expedition entry (same as fleet_idx), auto restart expedition
        @param index: expedition entry
        @type index: int
        @return: None
        @rtype: None
        """
        tab_exp = self.main_tabs.tabs.findChild(QWidget, 'tab_exp')
        tab_exp.fleet_table.start_expedition(index)

    def get_exp_result(self, exp_map: str) -> dict:
        def _get_res() -> Tuple[bool, dict]:
            data = self.api.getResult(exp_map)
            res = False
            if 'eid' in data:
                get_error(data['eid'])
            elif 'pveExploreVo' in data:
                res = True
            else:
                self.logger.debug(data)
            return res, data

        return self._reconnecting_calls(_get_res, 'collect expedition')

    def start_exp(self, exp_map: str, fleet_id: str) -> dict:
        def _start() -> Tuple[bool, dict]:
            data = self.api.start(exp_map, fleet_id)
            res = False
            if 'eid' in data:
                get_error(data['eid'])
            elif 'pveExploreVo' in data:
                res = True
            else:
                self.logger.debug(data)
            return res, data

        return self._reconnecting_calls(_start, 'start expedition')

    def cancel_exp(self, exp_map: str) -> dict:
        def _cancel() -> Tuple[bool, dict]:
            data = self.api.cancel(exp_map)
            res = False
            if 'eid' in data:
                get_error(data['eid'])
            elif 'status' in data:
                res = True
            else:
                self.logger.debug(data)
            return res, data

        return self._reconnecting_calls(_cancel, 'cancel expedition')


class TaskListView(AlignListView):
    def __init__(self):
        super().__init__()

    def on_single_click(self, index: QModelIndex) -> None:
        pass

    def on_double_click(self, index: QModelIndex) -> None:
        pass
        # task/getAward/{task_cid}

# End of File
