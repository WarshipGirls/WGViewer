
![alt text](docs/banner.png "Warship Girls Viewer | WGViewer")

![build](https://github.com/WarshipGirls/WGViewer/workflows/build/badge.svg)
![pytest](https://github.com/WarshipGirls/WGViewer/workflows/pytest/badge.svg)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

This project, `WGViewer`, is inspired by [Kancolle Viewer poi][poi] and [one of Warship Girls auto scripts][ProtectorMoe].
The goal of the project is to create a cross-desktop-platform game viewer and automation tool.

The official sites of the mobile game, Warship Girls (R), are [here (CN server)][CN], [here (JP server)][JP] and [here (International server)][Intl].

> NO STABLE RELEASE YET. PROJECT IS ON ACTIVE DEVELOPMENT  
> Developer version is ready via self compiling

## Screenshots

Please see [at this directory](screenshots). Updating as work progresses.

## Development

- [Python3](https://www.python.org/), [PyQt5](https://doc.qt.io/qtforpython/) (w/o Qt Designer), [PyInstaller](https://www.pyinstaller.org/)
- [Fiddler](https://www.telerik.com/download/fiddler)

### Compiling From Source

#### Windows

```
# 1. start a virtual environment
# 2. install required packages
> pip install -r requirements.txt
# 3. run auto build batch script
> win_build.bat
```

#### Unix

```
# 1. start a virtual environment
# 2. install required packages
> pip install -r requirements.txt
# 3. update fix_pyinstaller.py with your directory location, run
# 4. run commands
> python tools/fix_pyinstaller.py > gui_main.spec  
> pyinstaller --clean gui_main.spec
```

### Contribution

WGViewer welcomes contributors!

If you know "hello world" in any programming language, please see the [contribution guide](CONTRIBUTING.md) for more information.

If you don't know coding but still want to help WGViewer becomes better, you may
- upload missing ship images ([here](https://github.com/WarshipGirls/WGViewer/issues/43))
- add missing translations ([here](https://github.com/WarshipGirls/WGViewer/blob/master/src/func/shipname.py)).
- report bugs or make suggestions! ([here](https://github.com/WarshipGirls/WGViewer/issues))

## Disclaimer

The terms & conditions of this software can be found [here](DISCLAIMER.md)

## Licenses

The code is licensed under [GNU General Public License v3.0](https://github.com/WarshipGirls/WGViewer/blob/master/LICENSE)

The copyright of the shipgirl art resources used in the WGViewer belong to Moefantasy.

[poi]: https://github.com/poooi/poi
[ProtectorMoe]: https://github.com/ProtectorMoe
[CN]: http://www.jianniang.com/
[JP]: http://ssr.moefantasy.co.jp/
[Intl]: http://www.warshipgirls.com/en/