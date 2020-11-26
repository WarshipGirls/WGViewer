import ast
import re

from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtGui import  QIcon

from . import constant as SCONST


class ShipSortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, *args, **kwargs):
        QSortFilterProxyModel.__init__(self, *args, **kwargs)
        self.name_reg = None
        self.lock_opt = None
        self.level_opt = None
        self.mod_opt = None
        self.type_opt = None

        self.no_sort_cols = [0, 1, 3, 21, 22, 23, 24, 25, 26, 27]
        self.int_sort_cols = [2, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        self.float_sort_cols = [4]
        self.range_sort_col = [5]
        self.resource_sort_cols = [7, 17, 18, 19]
        self.slot_sort_col = [20]

    def setNameFilter(self, regex):
        '''
        reg = string, auto mapped to QString in Py3
        '''
        if isinstance(regex, str):
            regex = re.compile(regex)
        else:
            pass
        self.name_reg = regex
        self.invalidateFilter()

    def setLockFilter(self, is_lock):
        self.lock_opt = is_lock
        self.invalidateFilter()

    def setLevelFilter(self, level):
        self.level_opt = level
        self.invalidateFilter()

    def setModFilter(self, mod):
        self.mod_opt = mod
        self.invalidateFilter()

    def setTypeFilter(self, _type):
        self.type_opt = _type
        self.invalidateFilter()

    def _customFilterAcceptsRow(self, source_row, source_parent, opt, col, func):
        res = []
        if opt == None:
            res.append(source_row if source_row != 0 else True)
        else:
            idx = self.sourceModel().index(source_row, col, source_parent)
            if idx.isValid() == False:
                pass
            else:
                res = func(opt, idx)
        return res

    def nameFilterAcceptsRow(self, source_row, source_parent, opt, col):
        def f(o, i):
            r = []
            name = self.sourceModel().data(i, Qt.DisplayRole)
            if name == None:
                r.append(False)
            else:
                # https://docs.python.org/3/library/re.html#re.compile
                r.append(o.search(name))
            return r
        return self._customFilterAcceptsRow(source_row, source_parent, opt, col, f)

    def lockFilterAcceptsRow(self, source_row, source_parent, opt, col):
        def f(o, i):
            r = []
            lock = self.sourceModel().data(i, Qt.DecorationRole)   # Detect if have ICON
            if o == 'YES':
                r.append(isinstance(lock, QIcon))
            elif o == 'NO':
                r.append(not isinstance(lock, QIcon))
            else:
                r.append(True)
            return r
        return self._customFilterAcceptsRow(source_row, source_parent, opt, col, f)

    def levelFilterAcceptsRow(self, source_row, source_parent, opt, col):
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

    def modFilterAcceptsRow(self, source_row, source_parent, opt, col):
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

    def typeFilterAcceptsRow(self, source_row, source_parent, opt, col):
        def f(o, i):
            r = []
            t = self.sourceModel().data(i, Qt.UserRole)
            print(t)
            t = t[-2:]
            print(t)
            if o == "SMALL":
                r.append(t == "11")
            elif o == "MEDIUM":
                r.append(t == "12")
            elif o == "LARGE":
                r.append(t == "13")
            else:
                r.append(True)
            return r
        return self._customFilterAcceptsRow(source_row, source_parent, opt, col, f)

    def filterAcceptsRow(self, source_row, source_parent):
        '''
        overridden filterAcceptsRow(); virtual function
        return Boolean
        '''
        # Ensure all are `None`
        if False == any([self.name_reg, self.lock_opt, self.level_opt, self.mod_opt, self.type_opt]):
            return True

        # columns are HARDCODING
        name_res = self.nameFilterAcceptsRow(source_row, source_parent, self.name_reg, 1)
        if all(name_res) == False:
            return False
        else:
            pass
        lock_res = self.lockFilterAcceptsRow(source_row, source_parent, self.lock_opt, 2)
        if all(lock_res) == False:
            return False
        else:
            pass
        level_res = self.levelFilterAcceptsRow(source_row, source_parent, self.level_opt, 6)
        if all(level_res) == False:
            return False
        else:
            pass
        mod_res = self.modFilterAcceptsRow(source_row, source_parent, self.mod_opt, 0)
        if all(mod_res) == False:
            return False
        else:
            pass
        type_res = self.typeFilterAcceptsRow(source_row, source_parent, self.type_opt, 0)
        return all(type_res)

    def setFilterRegExp(self, string):
        return super().setFilterRegExp(string)

    def setFilterKeyColumn(self, column):
        return super().setFilterKeyColumn(column)

    def lessThan(self, source_left, source_right):
        if (source_left.isValid() and source_right.isValid()):
            l = source_left.data()
            r = source_right.data()
            if (source_left.column() in self.no_sort_cols):
                pass
            elif (source_left.column() in self.int_sort_cols):
                return int(l) < int(r)
            elif (source_left.column() in self.float_sort_cols):
                return float(l) < float(r)
            elif (source_left.column() in self.range_sort_col):
                return SCONST._range_to_int[l] < SCONST._range_to_int[r]
            elif (source_left.column() in self.resource_sort_cols):
                if (isinstance(l, str) == True) and ("/" in l):
                    return int(l[:l.find('/')]) < int(r[:r.find('/')]) 
                else:
                    return l < r
            elif (source_left.column() in self.slot_sort_col):
                    l = 0 if '-' in l else sum(ast.literal_eval(l))
                    r = 0 if '-' in r else sum(ast.literal_eval(r))
                    return l < r
            else:
                pass
        else:
            pass
        return super().lessThan(source_left, source_right)


# End of File