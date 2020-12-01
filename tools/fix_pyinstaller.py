import os

'''
The first argument is the location the resource will be available at in the packaged application
and the second is the location of the resource in the source directory.
This is not limited to just images either. Any file can be packaged along with the source code.
a.datas += [('images/icon.ico', 'D:\\[workspace]\\App\\src\\images\\icon.ico',  'DATA')]

# TO USE
Run this scripts, and copy paste output to the *.spec file. Do clean the old fix.
'''

spec_root = "\'D:\\\github\\\WGViewer\'"
def header(spec_root):
    t = """# -*- mode: python ; coding: utf-8 -*-
import sys
block_cipher = None
a = Analysis(['gui_main.py'],
             pathex=[{}],
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
""".format(spec_root)
    return t

def datas_import():
    excluding = ['.md', '.MD', '.zip', '.ZIP']
    os.chdir("..")
    root_dir = os.path.dirname(os.path.realpath(__file__))
    prefix_len = len(root_dir) + 1

    t = "a.datas += ["
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            file_name, file_extension = os.path.splitext(file)
            if file_extension in excluding:
                continue
            res = os.path.join(subdir, file)
            if "assets" in res:
                first = res[prefix_len:].replace("\\", "/")
                second = res.replace("\\", "\\\\")
                res_str = "('" + first + "','" + second + "','DATA'),\n"
                t += res_str
    t += "]"
    return t

def footer():
    t = """
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
          icon='assets/favicon.ico'
          )
"""
    return t

print(header(spec_root))
print(datas_import())
print(footer())