rm -rf build/
rm -rf dist/
cd tools/
C:\Users\Yanqi\AppData\Local\Programs\Python\Python37\python.exe fix_pyinstaller.py > ..\gui_main.spec
cd ..
pyinstaller.exe --clean gui_main.spec
pyinstaller.exe --clean gui_main.spec

