rm -rf build/
rm -rf dist/
cd tools/
SET mypath=%~dp0
echo %mypath:~0,-1%
echo "running fix_pyinstaller.py"
C:\Users\Yanqi\AppData\Local\Programs\Python\Python37\python.exe fix_pyinstaller.py > ..\gui_main.spec
cd ..
pyinstaller.exe --clean gui_main.spec
