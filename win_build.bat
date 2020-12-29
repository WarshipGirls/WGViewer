@echo ================================================
@echo      Warship Girls Viewer Windows Build
@echo ================================================
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

@rm -rf build/ dist/ wgv_venv/
python -m virtualenv wgv_venv
CALL %CD%\wgv_venv\Scripts\activate.bat
pip install -r requirements.txt
CD tools/
C:\Users\%uname%\AppData\Local\Programs\Python\%PyVer%\python.exe fix_pyinstaller.py > ..\gui_main.spec
CD ..
pyinstaller.exe --clean gui_main.spec
CALL %CD%\wgv_venv\Scripts\deactivate.bat
@goto :EOF
