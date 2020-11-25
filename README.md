# Warship Girls Viewer

This project is inspired by [Kancolle Viewer](https://github.com/poooi/poi) and [one of Warship Girls auto scripts](https://github.com/ProtectorMoe). The goal of this non-profitable open-source project is to create a cross-platform (Windows/Mac/Unix) game viewer and automation tool.

The official sites of the mobile game, Warship Girls (R), are [here (CN server)](http://www.jianniang.com/), [here (JP server)](http://ssr.moefantasy.co.jp/) and [here (International server)](http://www.warshipgirls.com/en/).

## Screenshot

Please see [at this directory](screenshots). Updating as work progresses.

## Development

- [Python3](https://www.python.org/)
- [PyQt5](https://doc.qt.io/qtforpython/) (w/o Qt Designer)
- Platforms:
	- Windows 10
	- Ubuntu 20.04

Nice tools to have:

- [Fiddler 4](https://www.telerik.com/fiddler)

### Contribution

To contribute code,

1. start a Python vitrual environment
2. install required packages:

> pip install -r requirements.txt

3. make a pull request when your code is ready :)

### Packing into executable

To build executable on Windows OS, run

> build.bat

To build executable on Unix OS, run

> pyinstaller --clean gui_main.spec

## Licenses

The copyright of the shipgirl art resources used in this project belongs to [MoeFantasy 幻萌网络](https://www.moefantasy.com/).

The code is licensed under [The MIT License](https://github.com/WarshipGirls/WGViewer/blob/master/LICENSE.txt).
