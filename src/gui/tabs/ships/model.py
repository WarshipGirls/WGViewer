import logging
import os
import re
import sys
import traceback

from PyQt5.QtCore import Qt, QVariant, pyqtSlot, QModelIndex
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QIcon

from . import constant as SCONST
from ....func import constants as CONST
from ....func.helper_function import Helper
from ....func import data as  wgr_data


def get_data_path(relative_path):
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


class ShipModel(QStandardItemModel):
    def __init__(self, view, api):
        super().__init__(view)
        # NOTE: `data()` is a method of `QStandardItemModel()`
        self.hlp = Helper()
        self.view = view
        self.api = api

        self.ships_S = []
        self.ships_M = []
        self.ships_L = []
        self.non_mods = []
        self.mods = []
        self.ships_raw_data = None

        self.value_opt = SCONST.value_select[0]

        self.headers = SCONST._header
        self.setColumnCount(len(self.headers))
        self.setHorizontalHeaderLabels(self.headers)
        self.init_icons()
        self.init_json()

    def init_icons(self):
        # To avoid repeatedly loading same icon, preload them
        self.ring_icon = QIcon(get_data_path("src/assets/icons/ring_60.png"))
        self.lock_icon = QIcon(get_data_path("src/assets/icons/lock_64.png"))

    def init_json(self):
        self.tactics_json = wgr_data.get_tactics_json()
        self.user_tactics = wgr_data.get_user_tactics()

    def set_data(self, _data):
        self.ships_raw_data = _data

        self.ships_data = []
        for i in range(27):
            self.ships_data.append([])
        for s in self.ships_raw_data:
            self.ships_data[s["type"]].append(s)
        for ship_type, ship_lists in enumerate(self.ships_data):
            if (ship_type not in CONST.ship_type) and (len(ship_lists) != 0):
                continue
            else:
                for ship in ship_lists:
                    self.insertRow(self.rowCount())
                    self.add_ship(self.rowCount()-1, ship)

    def add_ship(self, row, d):
        self.set_thumbnail(row, str(d["shipCid"]))
        self.set_name(row, d["title"], d["married"], d["create_time"], d["marry_time"])
        self.set_id(row, d["id"], d["isLocked"])
        self.set_class(row, d["type"])
        self.set_level(row, d["level"], d["exp"], d["nextExp"])

        self.set_stats(row, d["battleProps"], d["battlePropsMax"])
        self.set_slots(row, d["capacitySlotMax"], d["missileSlotMax"])
        self.set_equips(row, d["equipmentArr"])
        self.set_tactics(row, d['tactics'])

    def set_thumbnail(self, row, cid):
        ''' Column 0
        Set ship image (thumbnail) and categorize ships by cid along the way.
        '''
        assert (len(cid) == 8)

        if cid[-2:] == "11":
            self.ships_S.append(int(cid))
        elif cid[-2:] == "12":
            self.ships_M.append(int(cid))
        elif cid[-2:] == "13":
            self.ships_L.append(int(cid))
        else:
            err = "Unrecognized ship cid pattern: " + cid
            logging.warning(err)
            return None

        if cid[:3] == "100":
            prefix = "S_NORMAL_"
            self.non_mods.append(cid)
        elif cid[:3] == "110":
            prefix = "S_NORMAL_1"
            self.mods.append(cid)
        else:
            err = "Unrecognized ship cid pattern: " + cid
            logging.warning(err)
            return None

        # QTableWidgetItem requires unique assignment; thus, same pic cannot assign twice. Differ from QIcon
        img_path = "src/assets/S/" + prefix + str(int(cid[3:6])) + ".png"
        img = QPixmap()
        is_loaded =  img.load(get_data_path(img_path))
        if is_loaded:
            thumbnail = QStandardItem()
            thumbnail.setData(QVariant(img.scaled(78, 44)), Qt.DecorationRole)
            # hidden cid as Qt.UserRole
            thumbnail.setData(cid, Qt.UserRole)
            self.setItem(row, 0, thumbnail)
        else:
            tmp = QPixmap()
            tmp.load(get_data_path("src/assets/S/0v0.png"))
            tmp2 = QStandardItem()
            tmp2.setData(QVariant(tmp.scaled(78, 44)), Qt.DecorationRole)
            tmp2.setData(cid, Qt.UserRole)
            self.setItem(row, 0, tmp2)
            err = "Image path does not exist: " + img_path
            logging.warn(err)

    def set_name(self, *args):
        wig = QStandardItem(args[1])
        s = "Met on " + self.hlp.ts_to_date(args[3])
        if args[2] == 1:
            wig.setIcon(self.ring_icon)
            s += "\nMarried on " + self.hlp.ts_to_date(args[4])
        else:
            pass
        wig.setToolTip(s)
        self.setItem(args[0], 1, wig)

    def set_id(self, *args):
        wig = QStandardItem(str(args[1]))
        if args[2] == 1:
            wig.setIcon(self.lock_icon)
        else:
            # No icon for unlock as we uses QIcon/None to detect lock/unlock
            pass
        self.setItem(args[0], 2, wig)

    def set_class(self, *args):
        wig = QStandardItem(CONST.ship_type[args[1]])
        self.setItem(args[0], 3, wig)

    def set_level(self, *args):
        wig = QStandardItem(str(args[1]))

        if args[3] != -1:
            s = "Exp " + str(args[2]) + " / " + str(args[3])
            wig.setToolTip(s)
        else:
            pass
        self.setItem(args[0], 6, wig)

    @pyqtSlot(str)
    def on_stats_changed(self, *args):
        '''
        Getting check box update signal
        '''
        if args[0] in SCONST.value_select:
            self.value_opt = args[0]
        else:
            pass

        self.update_stats()

    def update_stats(self, *args):
        for row in range(self.rowCount()):
            _id_idx = self.index(row, 2, QModelIndex())
            _id = int(self.data(_id_idx, Qt.DisplayRole))
            _ship = next(i for i in self.ships_raw_data if i['id'] == _id)

            if self.value_opt == SCONST.value_select[0]:    # curr
                hp = str(_ship['battleProps']['hp']) + "/" + str(_ship['battlePropsMax']['hp'])
                oil = str(_ship['battleProps']['oil']) + "/" + str(_ship['battlePropsMax']['oil'])
                ammo = str(_ship['battleProps']['ammo']) + "/" + str(_ship['battlePropsMax']['ammo'])
                bauxite = str(_ship['battleProps']['aluminium']) + "/" + str(_ship['battlePropsMax']['aluminium'])
                self.item(row, 4).setData(_ship['battleProps']['speed'], Qt.DisplayRole)
                self.item(row, 5).setData(CONST.range_type[_ship['battleProps']['range']], Qt.DisplayRole)
                self.item(row, 7).setData(hp, Qt.DisplayRole)
                self.item(row, 8).setData(_ship['battleProps']['atk'], Qt.DisplayRole)
                self.item(row, 9).setData(_ship['battleProps']['def'], Qt.DisplayRole)
                self.item(row, 10).setData(_ship['battleProps']['torpedo'], Qt.DisplayRole)
                self.item(row, 11).setData(_ship['battleProps']['hit'], Qt.DisplayRole)
                self.item(row, 12).setData(_ship['battleProps']['miss'], Qt.DisplayRole)
                self.item(row, 13).setData(_ship['battleProps']['radar'], Qt.DisplayRole)
                self.item(row, 14).setData(_ship['battleProps']['airDef'], Qt.DisplayRole)
                self.item(row, 15).setData(_ship['battleProps']['antisub'], Qt.DisplayRole)
                self.item(row, 16).setData(_ship['battleProps']['luck'], Qt.DisplayRole)
                self.item(row, 17).setData(oil, Qt.DisplayRole)
                self.item(row, 18).setData(ammo, Qt.DisplayRole)
                self.item(row, 19).setData(bauxite, Qt.DisplayRole)
            elif self.value_opt == SCONST.value_select[1]:  # max
                self.item(row, 7).setData(_ship['battlePropsMax']['hp'], Qt.DisplayRole)
                self.item(row, 8).setData(_ship['battlePropsMax']['atk'], Qt.DisplayRole)
                self.item(row, 9).setData(_ship['battlePropsMax']['def'], Qt.DisplayRole)
                self.item(row, 10).setData(_ship['battlePropsMax']['torpedo'], Qt.DisplayRole)
                self.item(row, 11).setData(_ship['battlePropsMax']['hit'], Qt.DisplayRole)
                self.item(row, 12).setData(_ship['battlePropsMax']['miss'], Qt.DisplayRole)
                self.item(row, 13).setData(_ship['battlePropsMax']['radar'], Qt.DisplayRole)
                self.item(row, 15).setData(_ship['battlePropsMax']['antisub'], Qt.DisplayRole)
                self.item(row, 16).setData(_ship['battlePropsMax']['luck'], Qt.DisplayRole)
                self.item(row, 17).setData(_ship['battlePropsMax']['oil'], Qt.DisplayRole)
                self.item(row, 18).setData(_ship['battlePropsMax']['ammo'], Qt.DisplayRole)
                self.item(row, 19).setData(_ship['battlePropsMax']['aluminium'], Qt.DisplayRole)
            elif self.value_opt == SCONST.value_select[2]:  # raw
                self.item(row, 4).setData(_ship['battlePropsBasic']['speed'], Qt.DisplayRole)
                self.item(row, 5).setData(CONST.range_type[_ship['battlePropsBasic']['range']], Qt.DisplayRole)
                self.item(row, 7).setData(_ship['battlePropsBasic']['hp'], Qt.DisplayRole)
                self.item(row, 8).setData(_ship['battlePropsBasic']['atk'], Qt.DisplayRole)
                self.item(row, 9).setData(_ship['battlePropsBasic']['def'], Qt.DisplayRole)
                self.item(row, 10).setData(_ship['battlePropsBasic']['torpedo'], Qt.DisplayRole)
                self.item(row, 11).setData(_ship['battlePropsBasic']['hit'], Qt.DisplayRole)
                self.item(row, 12).setData(_ship['battlePropsBasic']['miss'], Qt.DisplayRole)
                self.item(row, 13).setData(_ship['battlePropsBasic']['radar'], Qt.DisplayRole)
                self.item(row, 14).setData(_ship['battlePropsBasic']['airDef'], Qt.DisplayRole)
                self.item(row, 15).setData(_ship['battlePropsBasic']['antisub'], Qt.DisplayRole)
                self.item(row, 16).setData(_ship['battlePropsBasic']['luck'], Qt.DisplayRole)
                self.item(row, 17).setData(_ship['battlePropsBasic']['oil'], Qt.DisplayRole)
                self.item(row, 18).setData(_ship['battlePropsBasic']['ammo'], Qt.DisplayRole)
                self.item(row, 19).setData(_ship['battlePropsBasic']['aluminium'], Qt.DisplayRole)
            else:
                pass

    def set_stats(self, *args):
        # set current ship stats as default
        
        # Design thinking: I thought set eye-catching color for not-full hp. 
        # but there will be dock in the future, so it is redundant to set color here
        # also extra work of set/reset-ing color
        hp = str(args[1]['hp']) + "/" + str(args[2]['hp'])
        wig_h = QStandardItem(hp)
        self.setItem(args[0], 7, wig_h)

        self.setItem(args[0], 4, QStandardItem(str(args[1]['speed'])))
        self.setItem(args[0], 5, QStandardItem(CONST.range_type[args[1]['range']]))
        self.setItem(args[0], 8, QStandardItem(str(args[1]['atk'])))
        self.setItem(args[0], 9, QStandardItem(str(args[1]['def'])))
        self.setItem(args[0], 10, QStandardItem(str(args[1]['torpedo'])))
        self.setItem(args[0], 11, QStandardItem(str(args[1]['hit'])))
        self.setItem(args[0], 12, QStandardItem(str(args[1]['miss'])))
        self.setItem(args[0], 13, QStandardItem(str(args[1]['radar'])))
        self.setItem(args[0], 14, QStandardItem(str(args[1]['airDef'])))
        self.setItem(args[0], 15, QStandardItem(str(args[1]['antisub'])))
        self.setItem(args[0], 16, QStandardItem(str(args[1]['luck'])))

        fuel = str(args[1]['oil']) + "/" + str(args[2]['oil'])
        wig_f = QStandardItem(fuel)
        self.setItem(args[0], 17, wig_f)
        ammo = str(args[1]['ammo']) + "/" + str(args[2]['ammo'])
        wig_a = QStandardItem(ammo)
        self.setItem(args[0], 18, wig_a)
        bauxite = str(args[1]['aluminium']) + "/" + str(args[2]['aluminium'])
        wig_b = QStandardItem(bauxite)
        self.setItem(args[0], 19, wig_b)

    def set_slots(self, *args):
        if (any(args[1]) and any(args[2])):
            slot = " - "
        else:
            if max(args[1]) > max(args[2]):
                slot = str(args[1])
            else:
                slot = str(args[2])

        wig = QStandardItem(slot)
        self.setItem(args[0], 20, wig)

    def set_equips(self, *args):

        col = 21
        for e in args[1]:
            e = str(e)
            if e == '-1':
                item = QStandardItem()
                item.setData(-1, Qt.UserRole)
                self.setItem(args[0], col, item)
                col += 1
                continue
            else:
                pass
            raw_path = "src/assets/E/equip_L_" + str(int(e[3:6])) + ".png"
            img_path = get_data_path(raw_path)

            img = QPixmap()
            is_loaded =  img.load(img_path)
            if is_loaded:
                thumbnail = QStandardItem()
                thumbnail.setData(QVariant(img), Qt.DecorationRole)
                thumbnail.setData(e, Qt.UserRole)   # hide Equipment cid
                self.setItem(args[0], col, thumbnail)
            else:
                logging.warning('Image for equipment {} is absent.'.format(e))
            col += 1

        rest = 4-len(args[1])
        for i in range(rest):
            item = QStandardItem('X')
            item.setFlags(Qt.NoItemFlags)
            self.setItem(args[0], col, item)
            col += 1

    def update_one_equip(self, row, col, equip_id):
        ship_id = self.index(row, 2).data()
        unequip_id = self.index(row, col).data(Qt.UserRole)
        equip_slot = col - 21

        if equip_id == "-1":
            # unequip; setItem deletes previous item
            item = QStandardItem()
            item.setData(-1, Qt.UserRole)
            self.setItem(row, col, item)
            wgr_data.update_equipment_amount(-1, unequip_id)
            self.api.boat_removeEquipment(ship_id, equip_slot)
            return
        else:
            pass

        res = self.api.boat_changeEquipment(ship_id, equip_id, equip_slot)
        if 'eid' not in res:
            # success
            wgr_data.update_equipment_amount(equip_id, unequip_id)
        else:
            logging.error('Equipment change is failed.')
            return

        raw_path = "src/assets/E/equip_L_" + str(int(equip_id[3:6])) + ".png"
        img_path = get_data_path(raw_path)
        img = QPixmap()
        is_loaded =  img.load(img_path)
        if is_loaded:
            thumbnail = QStandardItem()
            thumbnail.setData(QVariant(img), Qt.DecorationRole)
            thumbnail.setData(equip_id, Qt.UserRole)
            self.setItem(row, col, thumbnail)
        else:
            logging.warning('Image for equipment {} is absent.'.format(e))

    def set_tactics(self, *args):
        # stupid MoeFantasy makes it inefficient; can't access tactics LV by ship data
        # TODO: switch tactics like equip
        col = 25
        ship_id = self.index(args[0], 2).data()
        indices = wgr_data.find_all_indices(self.user_tactics, 'boat_id', ship_id)
        if len(indices) == 0:
            return
        else:
            pass

        for key in args[1]:
            t_id = int(args[1][key])
            if t_id == 0:
                pass
            else:
                for idx in indices:
                    if str(t_id) == str(self.user_tactics[idx]['cid'])[:-1]:
                        i = wgr_data.find_index(self.tactics_json, 'cid', self.user_tactics[idx]['cid'])
                        t = self.tactics_json[i]
                        title = t['title'] + " " + str(t['level'])
                        d1 = re.sub(r'\^.+?00000000', '', t["desc"])
                        d2 = re.sub(r'\^.+?00000000', '', t["desc2"])
                        desc = d1 + "\n" + d2

                        item = QStandardItem(title)
                        item.setToolTip(desc)
                        self.setItem(args[0], col, item)
                    else:
                        pass
            col += 1

    def set_skill(self):
        pass
         


# End of File