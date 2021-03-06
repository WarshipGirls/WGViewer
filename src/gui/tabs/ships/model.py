import os
import sys

from PyQt5.QtCore import Qt, QVariant, pyqtSlot
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QIcon
from PyQt5.QtWidgets import QTableView

from src import data as wgv_data
from src import utils as wgv_utils
from src.func import logger_names as QLOGS
from src.func.log_handler import get_logger
from src.wgr import API_BOAT
from . import constant as SCONST

logger = get_logger(QLOGS.TAB_SHIP)


def get_data_path(relative_path: str) -> str:
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


class ShipModel(QStandardItemModel):
    def __init__(self, view: QTableView):
        super().__init__(view)
        self.view = view
        self.api_boat = API_BOAT(wgv_data.load_cookies())

        self.value_opt = SCONST.value_select[0]
        self.headers = SCONST.header

        self.ring_icon = None
        self.lock_icon = None
        self.init_icons()
        self.tactics_json = None
        self.user_tactics = None
        self.init_json()

        self.ships_raw_data = None
        self.ships_data = []

        self.setColumnCount(len(self.headers))
        self.setHorizontalHeaderLabels(self.headers)

    def save_table_data(self) -> None:
        all_ships = {}
        for row in range(self.rowCount()):
            # Qt.DisplayRole (default), Qt.UserRole (hidden), Qt.DecorationRole (icon)
            s = {'cid': int(self.index(row, 0).data(Qt.UserRole)), 'Name': self.index(row, 1).data()}
            # Lesson: JSON keys have to be strings; json.dump() will convert int-key to str type
            all_ships[self.index(row, 2).data()] = s  # reference this dict
            for col in range(3, 21):  # str and str representation of int, float, list of int, int/int
                s[SCONST.header[col]] = self.index(row, col).data()
            equips = []  # equips cid (int), may contain None
            for col in range(21, 25):
                equips.append(self.index(row, col).data(Qt.UserRole))
            s['equips'] = equips
            tactics = []  # tactics cid (int), may contain None
            for col in range(25, 28):
                tactics.append(self.index(row, col).data(Qt.UserRole))
            s['tactics'] = tactics
            # TODO skill cid after implementing skill
        wgv_data.save_processed_userShipVo(all_ships)

    def init_icons(self) -> None:
        # To avoid repeatedly loading same icon, preload them
        self.ring_icon = QIcon(get_data_path("assets/icons/ring_60.png"))
        self.lock_icon = QIcon(get_data_path("assets/icons/lock_64.png"))

    def init_json(self) -> None:
        self.tactics_json = wgv_data.get_tactics_json()
        self.user_tactics = wgv_data.get_user_tactics()

    def set_data(self, _data: dict) -> None:
        self.ships_raw_data = _data

        for i in range(28):  # up to (not including) 28
            self.ships_data.append([])
        for s in self.ships_raw_data:
            self.ships_data[s["type"]].append(s)
        for ship_type, ship_lists in enumerate(self.ships_data):
            if (ship_type not in wgv_utils.get_all_ship_types()) and (len(ship_lists) != 0):
                continue
            else:
                for ship in ship_lists:
                    self.insertRow(self.rowCount())
                    self.add_ship(self.rowCount() - 1, ship)

    def add_ship(self, row: int, d: dict) -> None:
        logger.info(f"Populating {row}")
        self.set_thumbnail(row, str(d["shipCid"]))
        self.set_name(row, d["title"], d["married"], d["create_time"], d["marry_time"])
        self.set_id(row, d["id"], d["isLocked"])
        self.set_class(row, d["type"])
        self.set_level(row, d["level"], d["exp"], d["nextExp"])

        self.set_stats(row, d["battleProps"], d["battlePropsMax"])
        self.set_slots(row, d["capacitySlotMax"], d["missileSlotMax"])
        self.set_equips(row, d["equipmentArr"])
        self.set_tactics(row, d['tactics'])

    def set_thumbnail(self, row: int, cid: str) -> None:
        """ Column 0
        Set ship image (thumbnail) and categorize ships by cid along the way.
        """
        assert (len(cid) == 8)

        mid = str(int(cid[3:6]))
        if cid[:3] == "100":
            prefix = "S_NORMAL_"
        elif cid[:3] == "110":
            prefix = "S_NORMAL_1"
        elif cid[:2] == "18":
            prefix = "S_NORMAL_8"
            mid = mid.rjust(4, '0')[1:]
        else:
            err = "Unrecognized ship cid pattern: " + cid
            logger.warning(err)
            return None

        # QTableWidgetItem requires unique assignment; thus, same pic cannot assign twice. Differ from QIcon
        img_path = "S/" + prefix + mid + ".png"
        img = QPixmap()
        is_loaded = img.load(os.path.join(wgv_data.get_zip_dir(), get_data_path(img_path)))
        if is_loaded:
            thumbnail = QStandardItem()
            thumbnail.setData(QVariant(img.scaled(78, 44)), Qt.DecorationRole)
            # hidden cid as Qt.UserRole
            thumbnail.setData(cid, Qt.UserRole)
            self.setItem(row, 0, thumbnail)
        else:
            tmp = QPixmap()
            tmp.load(os.path.join(wgv_data.get_zip_dir(), get_data_path("S/0v0.png")))
            tmp2 = QStandardItem()
            tmp2.setData(QVariant(tmp.scaled(78, 44)), Qt.DecorationRole)
            tmp2.setData(cid, Qt.UserRole)
            self.setItem(row, 0, tmp2)
            err = "Image path does not exist: " + img_path
            logger.warning(err)

    def set_name(self, *args) -> None:
        wig = QStandardItem(args[1])
        s = "Met on " + wgv_utils.ts_to_date(int(args[3]))
        if args[2] == 1:
            wig.setIcon(self.ring_icon)
            s += "\nMarried on " + wgv_utils.ts_to_date(int(args[4]))
        else:
            pass
        wig.setToolTip(s)
        self.setItem(args[0], 1, wig)

    def set_id(self, *args) -> None:
        wig = QStandardItem(str(args[1]))
        if args[2] == 1:
            wig.setIcon(self.lock_icon)
        else:
            # No icon for unlock as we uses QIcon/None to detect lock/unlock
            pass
        self.setItem(args[0], 2, wig)

    def set_class(self, *args) -> None:
        wig = QStandardItem(wgv_utils.get_ship_type(args[1]))
        self.setItem(args[0], 3, wig)

    def set_level(self, *args) -> None:
        wig = QStandardItem(str(args[1]))

        if args[3] != -1:
            s = "Exp " + str(args[2]) + " / " + str(args[3])
            wig.setToolTip(s)
        else:
            pass
        self.setItem(args[0], 6, wig)

    @pyqtSlot(str)
    def on_stats_changed(self, *args) -> None:
        """
        Getting check box update signal
        """
        if args[0] in SCONST.value_select:
            self.value_opt = args[0]
        else:
            pass

        self.update_stats()

    def update_stats(self) -> None:
        for row in range(self.rowCount()):
            _id_idx = self.index(row, 2)
            _id = int(self.data(_id_idx, Qt.DisplayRole))
            _ship = next(i for i in self.ships_raw_data if i['id'] == _id)

            if self.value_opt == SCONST.value_select[0]:  # curr
                hp = str(_ship['battleProps']['hp']) + "/" + str(_ship['battlePropsMax']['hp'])
                oil = str(_ship['battleProps']['oil']) + "/" + str(_ship['battlePropsMax']['oil'])
                ammo = str(_ship['battleProps']['ammo']) + "/" + str(_ship['battlePropsMax']['ammo'])
                bauxite = str(_ship['battleProps']['aluminium']) + "/" + str(_ship['battlePropsMax']['aluminium'])
                self.item(row, 4).setData(_ship['battleProps']['speed'], Qt.DisplayRole)
                self.item(row, 5).setData(wgv_utils.get_ship_los(_ship['battleProps']['range']), Qt.DisplayRole)
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
                self.item(row, 5).setData(wgv_utils.get_ship_los(_ship['battlePropsBasic']['range']), Qt.DisplayRole)
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

    def set_stats(self, *args) -> None:
        # set current ship stats as default

        # Design thinking: I thought set eye-catching color for not-full hp. 
        # but there will be dock in the future, so it is redundant to set color here
        # also extra work of set/reset-ing color
        hp = str(args[1]['hp']) + "/" + str(args[2]['hp'])
        wig_h = QStandardItem(hp)
        self.setItem(args[0], 7, wig_h)

        self.setItem(args[0], 4, QStandardItem(str(args[1]['speed'])))
        self.setItem(args[0], 5, QStandardItem(wgv_utils.get_ship_los(args[1]['range'])))
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

    def set_slots(self, *args) -> None:
        if any(args[1]) and any(args[2]):
            slot = " - "
        else:
            if max(args[1]) > max(args[2]):
                slot = str(args[1])
            else:
                slot = str(args[2])

        wig = QStandardItem(slot)
        self.setItem(args[0], 20, wig)

    def set_equips(self, *args) -> None:

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
            raw_path = "E/equip_L_" + str(int(e[3:6])) + ".png"
            img_path = os.path.join(wgv_data.get_zip_dir(), get_data_path(raw_path))

            img = QPixmap()
            is_loaded = img.load(img_path)
            if is_loaded:
                thumbnail = QStandardItem()
                thumbnail.setData(QVariant(img), Qt.DecorationRole)
                thumbnail.setData(e, Qt.UserRole)  # hide Equipment cid
                self.setItem(args[0], col, thumbnail)
            else:
                logger.warning(f'Image for equipment {e} is absent.')
            col += 1

        rest = 4 - len(args[1])
        for i in range(rest):
            item = QStandardItem('X')
            item.setFlags(Qt.NoItemFlags)
            self.setItem(args[0], col, item)
            col += 1

    def update_one_equip(self, row: int, col: int, equip_id: int) -> None:
        ship_id = self.index(row, 2).data()
        unequip_id = self.index(row, col).data(Qt.UserRole)
        equip_slot = col - 21

        equip_id = str(equip_id)
        if equip_id == "-1":
            # unequip; setItem deletes previous item
            item = QStandardItem()
            item.setData(-1, Qt.UserRole)
            self.setItem(row, col, item)
            wgv_utils.update_equipment_amount(-1, unequip_id)
            self.api_boat.removeEquipment(str(ship_id), str(equip_slot))
            return
        else:
            pass

        res = self.api_boat.changeEquipment(str(ship_id), equip_id, str(equip_slot))
        if 'eid' not in res:
            # success
            wgv_utils.update_equipment_amount(int(equip_id), unequip_id)
        else:
            logger.error('Equipment change is failed.')
            return

        raw_path = "E/equip_L_" + str(int(equip_id[3:6])) + ".png"
        img_path = os.path.join(wgv_data.get_zip_dir(), get_data_path(raw_path))
        img = QPixmap()
        is_loaded = img.load(img_path)
        if is_loaded:
            thumbnail = QStandardItem()
            thumbnail.setData(QVariant(img), Qt.DecorationRole)
            thumbnail.setData(equip_id, Qt.UserRole)
            self.setItem(row, col, thumbnail)
        else:
            logger.warning(f'Image for equipment {equip_id} is absent.')

    def set_tactics(self, *args) -> None:
        # stupid MoeFantasy makes it inefficient; can't access tactics LV by ship data
        # TODO: switch tactics like equip
        col = 25
        ship_id = self.index(args[0], 2).data()
        indices = wgv_utils.find_all_indices(self.user_tactics, 'boat_id', ship_id)
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
                        i = wgv_utils.find_index(self.tactics_json, 'cid', self.user_tactics[idx]['cid'])
                        t = self.tactics_json[i]
                        title = t['title'] + " " + str(t['level'])
                        d1 = wgv_utils.clear_desc(t["desc"])
                        d2 = wgv_utils.clear_desc(t["desc2"])
                        desc = d1 + "\n" + d2

                        item = QStandardItem(title)
                        item.setData(self.user_tactics[idx]['cid'], Qt.UserRole)
                        item.setToolTip(desc)
                        self.setItem(args[0], col, item)
                    else:
                        pass
            col += 1

    def set_skill(self):
        # TODO
        pass

# End of File
