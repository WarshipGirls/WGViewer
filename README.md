# Warship Girls Viewer

This project is inspired by [Kancolle Viewer](https://github.com/poooi/poi) and [one of Warship Girls auto scripts](https://github.com/ProtectorMoe). The goal of this non-profitable open-source project is to create a cross-platform (Windows/Mac/Unix) game viewer and automation tool.

The official sites of the mobile game, Warship Girls (R), are [here (CN server)](http://www.jianniang.com/), [here (JP server)](http://ssr.moefantasy.co.jp/) and [here (International server)](http://www.warshipgirls.com/en/).

## Development

- [Python3](https://www.python.org/)
- [PyQt5](https://doc.qt.io/qtforpython/) (w/o Qt Designer)
- Platforms:
	- Windows 10
	- Ubuntu 20.04

## Screenshot

Please see [at this directory](screenshots). Updating as work progresses.

### Contribution

To contribute code,

1. start a Python vitrual environment
2. install required packages:

> pip install -r requirements.txt

To build executable on Windows OS, run

> build.bat

To build executable on Unix OS, run

> pyinstaller --clean gui_main.spec

Please check [this Mega TODO issue](https://github.com/WarshipGirls/WGViewer/issues/2) if you are interested in this project!

## Licenses

The copyright of the shipgirl art resources used in this project belongs to [MoeFantasy 幻萌网络](https://www.moefantasy.com/).

The code is licensed under [The MIT License](https://github.com/WarshipGirls/WGViewer/blob/master/LICENSE.txt).
