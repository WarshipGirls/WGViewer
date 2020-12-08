
![alt text](assets/banner.png "Warship Girls Viewer | WGViewer")

[![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/WarshipGirls/WGViewer?include_prereleases)](https://github.com/WarshipGirls/WGViewer/releases)
[![build](https://github.com/WarshipGirls/WGViewer/workflows/build/badge.svg)](https://github.com/WarshipGirls/WGViewer/actions?query=workflow%3Abuild)
[![pytest](https://github.com/WarshipGirls/WGViewer/workflows/pytest/badge.svg)](https://github.com/WarshipGirls/WGViewer/actions?query=workflow%3Apytest)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

[![GitHub issues](https://img.shields.io/github/issues/WarshipGirls/WGViewer)](https://github.com/WarshipGirls/WGViewer/issues)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/w/WarshipGirls/WGViewer)](https://github.com/WarshipGirls/WGViewer/graphs/contributors)
[![GitHub Org's stars](https://img.shields.io/github/stars/WarshipGirls?style=social)](https://github.com/WarshipGirls/WGViewer)
[![GitHub all releases](https://img.shields.io/github/downloads/WarshipGirls/WGViewer/total)](https://github.com/WarshipGirls/WGViewer/releases)

This project, `WGViewer`, is inspired by [Kancolle Viewer poi][poi] and [one of Warship Girls auto scripts][ProtectorMoe].
The goal of the project is to create a cross-desktop-platform game viewer and automation tool.
The idea is to hack the game and use its native APIs to mimic an official client's behaviors ([legal issue disclaimer](DISCLAIMER.md)).

The official sites of the mobile game, Warship Girls (R), are [here (CN)][CN], [here (JP)][JP] and [here (International)][Intl].

## Screenshots

Please see [at this directory](screenshots). Updating as work progresses.

## Development

- Primary:
    - [Python3](https://www.python.org/), [PyQt5](https://doc.qt.io/qtforpython/) (w/o Qt Designer), [PyInstaller](https://www.pyinstaller.org/)
- Secondary:    
    - [Fiddler](https://www.telerik.com/download/fiddler) (monitoring web traffic)
    - [HeroKu](https://www.heroku.com/) (host scheduled `WGViewer-tools` scripts)
    - [Docker](https://www.docker.com/) (use existing docker-image to package cross-platform `WGViewer`)

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
- upload missing ship images ([here](https://github.com/WarshipGirls/WGViewer/issues/43));
- add missing translations;
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