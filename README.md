# Warship Girls Viewer

> NO STABLE RELEASE YET. PROJECT IS ON ACTIVE DEVELOPMENT.

This project, `WGViewer`, is inspired by [Kancolle Viewer](https://github.com/poooi/poi) and [one of Warship Girls auto scripts](https://github.com/ProtectorMoe). The goal of the project is to create a cross-platform (Windows/Mac/Unix) game viewer and automation tool.

The official sites of the mobile game, Warship Girls (R), are [here (CN server)](http://www.jianniang.com/), [here (JP server)](http://ssr.moefantasy.co.jp/) and [here (International server)](http://www.warshipgirls.com/en/).

## Screenshots

Please see [at this directory](screenshots). Updating as work progresses.

## Development

- [Python3](https://www.python.org/)
- [PyQt5](https://doc.qt.io/qtforpython/) (w/o Qt Designer)
- Platforms:
	- Windows 10
	- Ubuntu 20.04

Nice tools to have: [Fiddler 4](https://www.telerik.com/fiddler), [Python debugger](https://docs.python.org/3/library/pdb.html).

### Contribution

To contribute code,

1. start a Python virtual environment
2. install required packages:

> pip install -r requirements.txt

3. make a pull request when your code is ready :)

### Packing into executable

To build executable on Windows OS, run

> build.bat

To build executable on Unix OS, run

> pyinstaller --clean gui_main.spec

## Disclaimer

Warship Girls Viewer (as "WGViewer") is not a representative and is not associated with Warship Girls (as "the game"), Warship Girls R (as "the game"), or [Moefantasy 幻萌网络](https://www.moefantasy.com/). The copyright of the shipgirl art resources used in the WGViewer belong to Moefantasy.

WGViewer is intended for educational purposes only. Botting is in violation of the User Agreement of the game; prolonged usage of WGViewer may result in your game account being banned. The developer of WGViewer takes no responsibility for repercussions related to the usage of WGViewer.

Although unlikely, users may sink ships and lose equipment when using WGViewer to conduct combat sorties. While WGViewer has been painstakingly designed to reduce chances of such occurrence, the developer of WGViewer does not take responsibility for any loss of ships and/or resources.

## Licenses

The code is licensed under [The MIT License](https://github.com/WarshipGirls/WGViewer/blob/master/LICENSE)
