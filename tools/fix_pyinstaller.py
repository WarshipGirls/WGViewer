import os
import sys
from pathlib import Path

'''
Example: a.datas += [('images/icon.ico', '[workspace]\\WGViewer\\src\\images\\icon.ico',  'DATA')]

The first argument is the location the resource will be available at in the packaged application
and the second is the location of the resource in the source directory.
This is not limited to just images either. Any file can be packaged along with the source code.
'''


SPEC_ROOT: str = os.path.split(Path().parent.absolute())[0]

CUSTOM_DATA_FILES: list = [
  "('docs/version_log.md','{}/docs/version_log.md','DATA'),".format(SPEC_ROOT)
]

def header(_spec_root: str) -> str:
    t = """# -*- mode: python ; coding: utf-8 -*-
import sys
block_cipher = None
a = Analysis(
  ['gui_main.py'],
  pathex=['{}'],
  binaries=[],
  datas=[],
  hiddenimports=[],
  hookspath=[],
  runtime_hooks=[],
  excludes=[],
  win_no_prefer_redirects=False,
  win_private_assemblies=False,
  cipher=block_cipher,
  noarchive=False
)
""".format(_spec_root)
    return t


def datas_import() -> str:
    excluding = ['.md', '.MD', '.zip', '.ZIP']
    os.chdir("..")
    root_dir = os.path.dirname(os.path.realpath(__file__))
    prefix_len = len(root_dir) + 1

    t = "a.datas += ["
    for c in CUSTOM_DATA_FILES:
      t += c
      t += "\n"

    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            file_name, file_extension = os.path.splitext(file)
            if file_extension in excluding:
                continue
            res = os.path.join(subdir, file)
            if "assets" in res:
                if sys.platform.startswith('win32'):
                    first = res[prefix_len:].replace("\\", "/")
                    second = res.replace("\\", "\\\\")
                elif sys.platform.startswith('linux'):
                    first = res[prefix_len:]
                    second = res
                else:
                    sys.exit('The OS is not supported yet. Please manually update.')
                res_str = "('" + first + "','" + second + "','DATA'),\n"
                t += res_str
    t += "]"
    return t


def footer() -> str:
    if sys.platform.startswith('win32'):
        name = 'WGViewer-win64.exe'
    elif sys.platform.startswith('linux'):
        name = 'WGViewer-linux64'
    else:
        sys.exit('The OS is not supported yet. Please manually update.')
    t = """
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
  a.scripts,
  a.binaries,
  a.zipfiles,
  a.datas,
  [],
  name='{}',
  debug=False,
  bootloader_ignore_signals=False,
  strip=False,
  upx=True,
  upx_exclude=[],
  runtime_tmpdir=None,
  console=False,
  icon='assets/favicon.ico'
)
""".format(name)
    return t


print(header(SPEC_ROOT))
print(datas_import())
print(footer())
