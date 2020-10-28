# -*- mode: python ; coding: utf-8 -*-
import sys

block_cipher = None


a = Analysis(['gui_main.py'],
             pathex=['D:\\github\\wgr-client\\gui'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

a.datas += [
('src/assets/dark_style.qss','D:\\github\\WGViewer\\src\\assets\\dark_style.qss','DATA'),
('src/assets/favicon.ico','D:\\github\\WGViewer\\src\\assets\\favicon.ico','DATA'),
('src/assets/icons/collect_16.png','D:\\github\\WGViewer\\src\\assets\\icons\\collect_16.png','DATA'),
('src/assets/icons/equip_16.png','D:\\github\\WGViewer\\src\\assets\\icons\\equip_16.png','DATA'),
('src/assets/icons/ship_16.png','D:\\github\\WGViewer\\src\\assets\\icons\\ship_16.png','DATA'),
('src/assets/icons/sign_16.png','D:\\github\\WGViewer\\src\\assets\\icons\\sign_16.png','DATA'),
('src/assets/items/ammo.png','D:\\github\\WGViewer\\src\\assets\\items\\ammo.png','DATA'),
('src/assets/items/bauxite.png','D:\\github\\WGViewer\\src\\assets\\items\\bauxite.png','DATA'),
('src/assets/items/BB.png','D:\\github\\WGViewer\\src\\assets\\items\\BB.png','DATA'),
('src/assets/items/blueprint_construct.png','D:\\github\\WGViewer\\src\\assets\\items\\blueprint_construct.png','DATA'),
('src/assets/items/blueprint_dev.png','D:\\github\\WGViewer\\src\\assets\\items\\blueprint_dev.png','DATA'),
('src/assets/items/CA.png','D:\\github\\WGViewer\\src\\assets\\items\\CA.png','DATA'),
('src/assets/items/CV.png','D:\\github\\WGViewer\\src\\assets\\items\\CV.png','DATA'),
('src/assets/items/DD.png','D:\\github\\WGViewer\\src\\assets\\items\\DD.png','DATA'),
('src/assets/items/fuel.png','D:\\github\\WGViewer\\src\\assets\\items\\fuel.png','DATA'),
('src/assets/items/gold.png','D:\\github\\WGViewer\\src\\assets\\items\\gold.png','DATA'),
('src/assets/items/instant_build.png','D:\\github\\WGViewer\\src\\assets\\items\\instant_build.png','DATA'),
('src/assets/items/instant_repair.png','D:\\github\\WGViewer\\src\\assets\\items\\instant_repair.png','DATA'),
('src/assets/items/revive.png','D:\\github\\WGViewer\\src\\assets\\items\\revive.png','DATA'),
('src/assets/items/SS.png','D:\\github\\WGViewer\\src\\assets\\items\\SS.png','DATA'),
('src/assets/items/steel.png','D:\\github\\WGViewer\\src\\assets\\items\\steel.png','DATA'),
]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Warship Girls Viewer' + ('.exe' if sys.platform == 'win32' else ''),
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon='src/assets/favicon.ico'
          )
