# Warship Girls Viewer

[![license:gpl-3.0](https://img.shields.io/badge/license-GPLv3-brightgreen)](https://opensource.org/licenses/GPL-3.0)

> NO STABLE RELEASE YET. PROJECT IS ON ACTIVE DEVELOPMENT.

This project, `WGViewer`, is inspired by [Kancolle Viewer](https://github.com/poooi/poi) and [one of Warship Girls auto scripts](https://github.com/ProtectorMoe). The goal of the project is to create a cross-platform (Windows/Mac/Unix) game viewer and automation tool.

The official sites of the mobile game, Warship Girls (R), are [here (CN server)](http://www.jianniang.com/), [here (JP server)](http://ssr.moefantasy.co.jp/) and [here (International server)](http://www.warshipgirls.com/en/).

## Screenshots

Please see [at this directory](screenshots). Updating as work progresses.

## Development

- [Python3](https://www.python.org/), [PyQt5](https://doc.qt.io/qtforpython/) (w/o Qt Designer), [PyInstaller](https://www.pyinstaller.org/)
- Windows 10, Ubuntu 20.04

### Contribution

To contribute code,

1. start a Python virtual environment
2. install required packages: `pip install -r requirements.txt`
3. make a [pull request](../../pulls) when your code is ready :)

### Packing into executable

To build executable on Windows OS, run

> win_build.bat

To build executable on Unix OS, update `fix_pyinstaller.py` with your directory location, run

> python tools/fix_pyinstaller.py > gui_main.spec  
> pyinstaller --clean gui_main.spec

## Disclaimer

The terms & conditions of this software can be found [here](DISCLAIMER.md)

## Licenses

The code is licensed under [GNU General Public License v3.0](https://github.com/WarshipGirls/WGViewer/blob/master/LICENSE)

The copyright of the shipgirl art resources used in the WGViewer belong to Moefantasy.
