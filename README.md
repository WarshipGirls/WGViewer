
![alt text](assets/banner.png "Warship Girls Viewer | WGViewer")

[![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/WarshipGirls/WGViewer?include_prereleases)](https://github.com/WarshipGirls/WGViewer/releases)
[![build](https://github.com/WarshipGirls/WGViewer/workflows/build/badge.svg)](https://github.com/WarshipGirls/WGViewer/actions?query=workflow%3Abuild)
[![pytest](https://github.com/WarshipGirls/WGViewer/workflows/pytest/badge.svg)](https://github.com/WarshipGirls/WGViewer/actions?query=workflow%3Apytest)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

[![GitHub issues](https://img.shields.io/github/issues/WarshipGirls/WGViewer)](https://github.com/WarshipGirls/WGViewer/issues)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/w/WarshipGirls/WGViewer)](https://github.com/WarshipGirls/WGViewer/graphs/contributors)
[![GitHub Org's stars](https://img.shields.io/github/stars/WarshipGirls?style=social)](https://github.com/WarshipGirls/WGViewer)
[![GitHub all releases](https://img.shields.io/github/downloads/WarshipGirls/WGViewer/total)](https://github.com/WarshipGirls/WGViewer/releases)

> This project is ARCHIVED due to the complete frame update of the game (v5.3.0). The hacking mathod used in this project is outdated.

This project, `WGViewer`, is inspired by [Kancolle Viewer poi][poi] and [one of Warship Girls auto scripts][ProtectorMoe].
The goal of the project is to create a cross-desktop-platform game viewer and automation tool.
The idea is to hack the game and use its native APIs to mimic an official client's behaviors ([legal issue disclaimer](DISCLAIMER.md)).

The official sites of the mobile game, Warship Girls (R), are [here (CN)][CN], [here (JP)][JP] and [here (International)][Intl].

## Main Features

As of `v0.2.3dev` ([commit 4a366e7c][commit-url]),

- Auto sortie on Thermopylae Ex-6, with user customized fleet
- Auto (& Manual) perform expedition tasks
- Display all warships' statistics, with sorting & filtering
- Display all user's docking/constructing/developing/tasking info on side panel
- Logs user's resources, with interactive data graphs

## Screenshots

Please see [at this directory](screenshots). Updating as work progresses.

## Download

| OS          | WGViewer version | Download Links        | Size    | Comment |
|:-----------:|:----------------:|:---------------------:|:-------:|:-------:|
| Windows x64 | 0.2.3.1dev       | [GH release][d-win]   | ~113 MB |         |
| Linux x64   | 0.2.1dev         | [GH release][d-linux] | ~70 MB  | unzip it and run on CLI |

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
# 1. run auto build batch script
> win_build.bat
# 2. Run the application
> dist\WGViewer-win64.exe
```

#### Unix

```
# 1. run auto build bash script
> $ ./linux_build.sh
# 2. Run the application
> $ ./dist/WGViewer-linux64
```

### Contribution

WGViewer welcomes contributors!

If you know "hello world" in any programming language, please see the [contribution guide](.github/CONTRIBUTING.md) for more information.

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
[commit-url]: https://github.com/WarshipGirls/WGViewer/tree/4a366e7c45a6e0e9e2116e04f94980b7e88b821f

[d-win]: https://github.com/WarshipGirls/WGViewer/releases/download/v0.2.3.1-dev/WGViewer-win64.zip
[d-linux]: https://github.com/WarshipGirls/WGViewer/releases/download/v0.2.1-dev/WGViewer-linux64.zip
