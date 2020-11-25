import ast
import re

from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtGui import  QIcon

from . import ships_constant as SCONST

class ShipSortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, *args, **kwargs):
        QSortFilterProxyModel.__init__(self, *args, **kwargs)
        self.name_reg = None
        self.lock_opt = None
        self.level_opt = None
        # self.lock_opt = 'ALL'
        self.no_sort_cols = [0, 21, 22, 23, 24, 25, 26, 27]
        self.int_sort_cols = [1, 2, 3, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16]
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

    def filterAcceptsRow(self, source_row, source_parent):
        '''
        overridden filterAcceptsRow(); virtual function
        return Boolean
        '''
        if self.name_reg == None and self.lock_opt == None and self.level_opt == None:
            return True

        name_res = []
        if self.name_reg == None:
            name_res.append(source_row if source_row != 0 else True)
        else:
            name = ""
            name_col = 1
            name_index = self.sourceModel().index(source_row, name_col, source_parent)
            if name_index.isValid() == False:
                pass
            else:
                name = self.sourceModel().data(name_index, Qt.DisplayRole)
                if name == None:
                    name = ""
                else:
                    pass
            # https://docs.python.org/3/library/re.html#re.compile
            name_res.append(self.name_reg.search(name))
        res = all(name_res)
        if res == False:
            return False
        else:
            pass

        lock_res = []
        if self.lock_opt == None or self.lock_opt == 'ALL':
            lock_res.append(source_row if source_row != 0 else True)
        else:
            lock_col = 2
            lock_index = self.sourceModel().index(source_row, lock_col, source_parent)
            if lock_index.isValid() == False:
                pass
            else:
                lock = self.sourceModel().data(lock_index, Qt.DecorationRole)   # Detect if have ICON
                if self.lock_opt == 'YES':
                    lock_res.append(isinstance(lock, QIcon))
                elif self.lock_opt == 'NO':
                    lock_res.append(not isinstance(lock, QIcon))
                else:
                    pass

        res = res and all(lock_res)
        if res == False:
            return False
        else:
            pass

        level_res = []
        if self.level_opt == None or self.level_opt == 'ALL':
            level_res.append(source_row if source_row != 0 else True)
        else:
            level_col = 4
            level_index = self.sourceModel().index(source_row, level_col, source_parent)
            if level_index.isValid() == False:
                pass
            else:
                level = self.sourceModel().data(level_index, Qt.DisplayRole)
                if self.level_opt == 'Lv. 1':
                    level_res.append(int(level) == 1)
                elif self.level_opt == "> Lv. 1":
                    level_res.append(int(level) > 1)
                elif self.level_opt == "\u2265 Lv. 90":
                    level_res.append(int(level) >= 90)
                elif self.level_opt == "\u2265 Lv. 100":
                    level_res.append(int(level) >= 100)
                elif self.level_opt == "= Lv. 110":
                    level_res.append(int(level) == 110)
                else:
                    pass

        res = res and all(level_res)
        return res

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