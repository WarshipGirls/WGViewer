# Warship Girls Viewer

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
3. make a [pull request](pulls) when your code is ready :)

### Packing into executable

To build executable on Windows OS, run

> win_build.bat

To build executable on Unix OS, update `fix_pyinstaller.py` with your directory location, run

> python tools/fix_pyinstaller.py > gui_main.spec  
> pyinstaller --clean gui_main.spec

## Contributors

[![](https://sourcerer.io/fame/pwyq/WarshipGirls/WGViewer/images/0)](https://sourcerer.io/fame/pwyq/WarshipGirls/WGViewer/links/0)
[![](https://sourcerer.io/fame/pwyq/WarshipGirls/WGViewer/images/1)](https://sourcerer.io/fame/pwyq/WarshipGirls/WGViewer/links/1)
[![](https://sourcerer.io/fame/pwyq/WarshipGirls/WGViewer/images/2)](https://sourcerer.io/fame/pwyq/WarshipGirls/WGViewer/links/2)
[![](https://sourcerer.io/fame/pwyq/WarshipGirls/WGViewer/images/3)](https://sourcerer.io/fame/pwyq/WarshipGirls/WGViewer/links/3)
[![](https://sourcerer.io/fame/pwyq/WarshipGirls/WGViewer/images/4)](https://sourcerer.io/fame/pwyq/WarshipGirls/WGViewer/links/4)
[![](https://sourcerer.io/fame/pwyq/WarshipGirls/WGViewer/images/5)](https://sourcerer.io/fame/pwyq/WarshipGirls/WGViewer/links/5)
[![](https://sourcerer.io/fame/pwyq/WarshipGirls/WGViewer/images/6)](https://sourcerer.io/fame/pwyq/WarshipGirls/WGViewer/links/6)
[![](https://sourcerer.io/fame/pwyq/WarshipGirls/WGViewer/images/7)](https://sourcerer.io/fame/pwyq/WarshipGirls/WGViewer/links/7)

## Disclaimer

The terms & conditions of this software can be found [here](DISCLAIMER.md)

## Licenses

The code is licensed under [The MIT License](https://github.com/WarshipGirls/WGViewer/blob/master/LICENSE)
