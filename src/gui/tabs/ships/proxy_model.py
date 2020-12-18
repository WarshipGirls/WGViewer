import ast
import re
from typing import Callable

from PyQt5.QtCore import Qt, QSortFilterProxyModel, QModelIndex, QRegExp
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QCheckBox

from src import data as wgv_data
from src.func import logger_names as QLOGS
from src.func.log_handler import get_logger
from . import constant as SCONST

logger = get_logger(QLOGS.DATA)


class ShipSortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, *args, **kwargs):
        QSortFilterProxyModel.__init__(self, *args, **kwargs)
        self.name_reg = None
        self.lock_opt = None
        self.level_opt = None
        self.mod_opt = None
        self.type_size_opt = None
        self.rarity_opt = None
        self.marry_opt = None
        self.country_opt = None

        self.checkboxes_opt = {}
        # LESSON: Unlike C++, Python have no reference to a variable, so following will create self.all_opts points
        # to [None, ...] which will remain unchanged and will fail filtering self.all_opts = [self.name_reg, ...]

        self.no_sort_cols = [0, 1, 3, 21, 22, 23, 24, 25, 26, 27]
        self.int_sort_cols = [2, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        self.float_sort_cols = [4]
        self.range_sort_col = [5]
        self.resource_sort_cols = [7, 17, 18, 19]
        self.slot_sort_col = [20]

        # TODO? multi-processing following command
        self._info = wgv_data.init_ships_temp()
        logger.debug('Proxy Model init done.')

    def ship_id_to_rarity(self, cid: int) -> int:
        try:
            return self._info[str(cid)]['rarity']
        except KeyError:
            logger.error(f'proxy {cid} not exist!')

    def ship_id_to_country(self, cid: int) -> int:
        try:
            return self._info[str(cid)]['country']
        except KeyError:
            logger.error(f'proxy {cid} not exist!')

    def set_name_filter(self, regex: str) -> None:
        """
        reg = string, auto mapped to QString in Py3
        """
        if isinstance(regex, str):
            regex = re.compile(regex)
        else:
            pass
        self.name_reg = regex
        self.invalidateFilter()

    def set_lock_filter(self, is_lock: [None, str]) -> None:
        self.lock_opt = is_lock
        self.invalidateFilter()

    def set_level_filter(self, level: [None, str]) -> None:
        self.level_opt = level
        self.invalidateFilter()

    def set_mod_filter(self, mod: [None, str]) -> None:
        self.mod_opt = mod
        self.invalidateFilter()

    def set_type_filter(self, type_size: [None, str]) -> None:
        self.type_size_opt = type_size
        self.invalidateFilter()

    def set_rarity_filter(self, rarity: [None, str]) -> None:
        self.rarity_opt = rarity
        self.invalidateFilter()

    def set_marry_filter(self, married: [None, str]) -> None:
        self.marry_opt = married
        self.invalidateFilter()

    def set_country_filter(self, country: [None, str]) -> None:
        self.country_opt = country
        self.invalidateFilter()

    def set_checkbox_filter(self, x: [None, QCheckBox]) -> None:
        if x is None:
            self.checkboxes_opt = {}
        else:
            self.checkboxes_opt[x.text()] = x.isChecked()
        self.invalidateFilter()

    def _customFilterAcceptsRow(self, source_row: int, source_parent: QModelIndex, opt: str, col: int, func: Callable) -> list:
        res = []
        if opt is None:
            res.append(source_row if source_row != 0 else True)
        else:
            idx = self.sourceModel().index(source_row, col, source_parent)
            if not idx.isValid():
                pass
            else:
                res = func(opt, idx)
        return res

    def checkboxFilterAcceptsRow(self, source_row: int, source_parent: QModelIndex, opt: dict, col: int) -> list:
        res = []
        if not any(opt):
            res.append(source_row if source_row != 0 else True)
        else:
            idx = self.sourceModel().index(source_row, col, source_parent)
            if not idx.isValid():
                pass
            else:
                ship_class = self.sourceModel().data(idx, Qt.DisplayRole)
                if ship_class not in opt:
                    res.append(False)
                else:
                    res.append(opt[ship_class] == True)
        return res

    def nameFilterAcceptsRow(self, source_row: int, source_parent: QModelIndex, opt: str, col: int) -> list:
        def f(o, i):
            r = []
            name = self.sourceModel().data(i, Qt.DisplayRole)
            if name is None:
                r.append(False)
            else:
                # https://docs.python.org/3/library/re.html#re.compile
                r.append(o.search(name))
            return r

        return self._customFilterAcceptsRow(source_row, source_parent, opt, col, f)

    def lockFilterAcceptsRow(self, source_row: int, source_parent: QModelIndex, opt: str, col: int) -> list:
        def f(o, i):
            r = []
            lock = self.sourceModel().data(i, Qt.DecorationRole)  # Detect if have ICON
            if o == 'YES':
                r.append(isinstance(lock, QIcon))
            elif o == 'NO':
                r.append(not isinstance(lock, QIcon))
            else:
                r.append(True)
            return r

        return self._customFilterAcceptsRow(source_row, source_parent, opt, col, f)

    def levelFilterAcceptsRow(self, source_row: int, source_parent: QModelIndex, opt: str, col: int) -> list:
        def f(o, i):
            r = []
            level = self.sourceModel().data(i, Qt.DisplayRole)
            if o == 'Lv. 1':
                r.append(int(level) == 1)
            elif o == "> Lv. 1":
                r.append(int(level) > 1)
            elif o == "\u2265 Lv. 90":
                r.append(int(level) >= 90)
            elif o == "\u2265 Lv. 100":
                r.append(int(level) >= 100)
            elif o == "= Lv. 110":
                r.append(int(level) == 110)
            else:
                r.append(True)
            return r

        return self._customFilterAcceptsRow(source_row, source_parent, opt, col, f)

    def modFilterAcceptsRow(self, source_row: int, source_parent: QModelIndex, opt: str, col: int) -> list:
        def f(o, i):
            r = []
            mod = self.sourceModel().data(i, Qt.UserRole)[:3]
            if o == "Non-mod.":
                r.append(mod == "100")
            elif o == "Mod. I":
                r.append(mod == "110")
            else:
                r.append(True)
            return r

        return self._customFilterAcceptsRow(source_row, source_parent, opt, col, f)

    def sizeFilterAcceptsRow(self, source_row: int, source_parent: QModelIndex, opt: str, col: int) -> list:
        def f(o, i):
            r = []
            s = self.sourceModel().data(i, Qt.UserRole)[-2:]
            if o == "SMALL":
                r.append(s == "11")
            elif o == "MEDIUM":
                r.append(s == "12")
            elif o == "LARGE":
                r.append(s == "13")
            else:
                r.append(True)
            return r

        return self._customFilterAcceptsRow(source_row, source_parent, opt, col, f)

    def typeFilterAcceptsRow(self, source_row: int, source_parent: QModelIndex, opt: str, col: int) -> list:
        def f(o, i):
            r = []
            t = self.sourceModel().data(i, Qt.DisplayRole)
            if o == "FLAGSHIP":
                r.append(t in SCONST.flagships)
            elif o == "ESCORT":
                r.append(t in SCONST.escorts)
            elif o == "SUB":
                r.append(t in SCONST.subs)
            else:
                r.append(True)
            return r

        return self._customFilterAcceptsRow(source_row, source_parent, opt, col, f)

    def rarityFilterAcceptsRow(self, source_row: int, source_parent: QModelIndex, opt: str, col: int) -> list:
        def f(o, i):  # o is QComboBox index
            res = []
            cid = self.sourceModel().data(i, Qt.UserRole)
            rarity = self.ship_id_to_rarity(cid)
            if o == 0:
                res.append(True)
            else:
                res.append(o == rarity)
            return res

        return self._customFilterAcceptsRow(source_row, source_parent, opt, col, f)

    def countryFilterAcceptsRow(self, source_row: int, source_parent: QModelIndex, opt: str, col: int) -> list:
        def f(o, i):  # o is QComboBox index
            res = []
            cid = self.sourceModel().data(i, Qt.UserRole)
            country = self.ship_id_to_country(cid)
            if o in [0, 9, 10]:
                res.append(True)
            else:
                res.append(o == country)
            return res

        return self._customFilterAcceptsRow(source_row, source_parent, opt, col, f)

    # ================================================================
    # QSortFilterProxyModel virtual functions
    # ================================================================

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:

        cond1 = False == any(self.checkboxes_opt)
        cond2 = False == any(
            [self.name_reg, self.lock_opt, self.level_opt, self.mod_opt, self.type_size_opt, self.rarity_opt,
             self.marry_opt, self.country_opt])
        if cond1 and cond2:
            return True
        else:
            pass

        checkbox_res = self.checkboxFilterAcceptsRow(source_row, source_parent, self.checkboxes_opt, 3)
        if not all(checkbox_res):
            return False
        else:
            pass

        # columns are HARDCODING
        name_res = self.nameFilterAcceptsRow(source_row, source_parent, self.name_reg, 1)
        if not all(name_res):
            return False
        else:
            pass

        lock_res = self.lockFilterAcceptsRow(source_row, source_parent, self.lock_opt, 2)
        if not all(lock_res):
            return False
        else:
            pass

        level_res = self.levelFilterAcceptsRow(source_row, source_parent, self.level_opt, 6)
        if not all(level_res):
            return False
        else:
            pass

        mod_res = self.modFilterAcceptsRow(source_row, source_parent, self.mod_opt, 0)
        if not all(mod_res):
            return False
        else:
            pass

        size_res = self.sizeFilterAcceptsRow(source_row, source_parent, self.type_size_opt, 0)
        type_res = self.typeFilterAcceptsRow(source_row, source_parent, self.type_size_opt, 3)
        type_size_res = all(size_res) and all(type_res)
        if not type_size_res:
            return False
        else:
            pass

        rarity_res = self.rarityFilterAcceptsRow(source_row, source_parent, self.rarity_opt, 0)
        if not all(rarity_res):
            return False
        else:
            pass

        # marryFilter shares same code as lockFilter
        marry_res = self.lockFilterAcceptsRow(source_row, source_parent, self.marry_opt, 1)
        if not all(marry_res):
            return False
        else:
            pass

        country_res = self.countryFilterAcceptsRow(source_row, source_parent, self.country_opt, 0)
        return all(country_res)

    def setFilterRegExp(self, string: QRegExp) -> None:
        return super().setFilterRegExp(string)

    def setFilterKeyColumn(self, column: int) -> None:
        return super().setFilterKeyColumn(column)

    def lessThan(self, source_left: QModelIndex, source_right: QModelIndex) -> bool:
        if source_left.isValid() and source_right.isValid():
            l = source_left.data()
            r = source_right.data()
            if source_left.column() in self.no_sort_cols:
                pass
            elif source_left.column() in self.int_sort_cols:
                return int(l) < int(r)
            elif source_left.column() in self.float_sort_cols:
                return float(l) < float(r)
            elif source_left.column() in self.range_sort_col:
                return SCONST.range_to_int[l] < SCONST.range_to_int[r]
            elif source_left.column() in self.resource_sort_cols:
                if (isinstance(l, str) == True) and ("/" in l):
                    return int(l[:l.find('/')]) < int(r[:r.find('/')])
                else:
                    return l < r
            elif source_left.column() in self.slot_sort_col:
                l = 0 if '-' in l else sum(ast.literal_eval(l))
                r = 0 if '-' in r else sum(ast.literal_eval(r))
                return l < r
            else:
                pass
        else:
            pass
        return super().lessThan(source_left, source_right)

# End of File
