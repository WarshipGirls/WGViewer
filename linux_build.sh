#!/bin/bash
verlte() {
    [  "$1" = "`echo -e "$1\n$2" | sort -V | head -n1`" ]
}

verlt() {
    [ "$1" = "$2" ] && return 1 || verlte $1 $2
}
echo ================================================
echo        Warship Girls Viewer Linux Build
echo ================================================
version="$(python3 -c 'import platform; print(platform.python_version())')"
yes="Required Python 3.6.0+ is not installed on your system. Your version=$version"
no="Python version check passed"
verlt $version 3.6.0 && echo $yes && exit 1 || echo $no

rm -rf ./build/ ./dist/ ./wgv_venv
python3 -m virtualenv --python=python3 wgv_venv
source wgv_venv/bin/activate
pip install -r ./linux_requirements.txt
cd tools
python3 fix_pyinstaller.py > ../gui_main.spec
cd ..
pyinstaller gui_main.spec
deactivate
cd ./dist
zip WGViewer-linux64.zip WGViewer-linux64
