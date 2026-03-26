@echo off
setlocal
cd /d "%~dp0"

if not exist "venv\Scripts\python.exe" (
    echo Missing Windows virtual environment: venv\Scripts\python.exe
    exit /b 1
)

if not exist "exports" mkdir "exports"

call "venv\Scripts\python.exe" -m pip install -r requirements.txt pyinstaller
if errorlevel 1 exit /b %errorlevel%

call "venv\Scripts\python.exe" -m PyInstaller --noconfirm "Hull_Variants.spec"
if errorlevel 1 exit /b %errorlevel%

if not exist "dist\exports" mkdir "dist\exports"

echo.
echo Build complete.
echo Executable: dist\Hull Variants.exe
echo Exports:    dist\exports\
endlocal
