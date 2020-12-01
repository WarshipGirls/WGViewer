@echo ================================================
@echo      Warship Girls Viewer Windows Build
@echo ================================================
@rm -rf build/
@rm -rf dist/
@cd tools/
goto :DOES_PYTHON_EXIST
:DOES_PYTHON_EXIST
python -V | find /v "Python" >NUL 2>NUL && (goto :PYTHON_DOES_NOT_EXIST)
python -V | find "Python"    >NUL 2>NUL && (goto :PYTHON_DOES_EXIST)
goto :EOF
:PYTHON_DOES_NOT_EXIST
@echo Python is not installed on your system.
@echo Now opeing the download URL.
start "" "https://www.python.org/downloads/windows/"
goto :EOF
:PYTHON_DOES_EXIST
@for /f "delims=" %%V in ('python -V') do @set ver=%%V
@SET PyVer=%ver:~0,6%%ver:~7,1%%ver:~9,1%
@Rem Win10 truncate username to 5 letters
@SET uname=%username:~0,5%
C:\Users\%uname%\AppData\Local\Programs\Python\%PyVer%\python.exe fix_pyinstaller.py > ..\gui_main.spec
@cd ..
pyinstaller.exe --clean gui_main.spec
@goto :EOF
