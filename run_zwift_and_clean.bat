@echo off
setlocal

REM === 1. Change to the script’s own directory ===
cd /d "%~dp0"

REM === 2. Get Zwift path from constants.py ===
for /f "usebackq delims=" %%A in (
    `python -c "from constants import ZWIFT_EXECUTABLE_PATH; print(ZWIFT_EXECUTABLE_PATH)"`
) do set "ZWIFT_EXECUTABLE_PATH=%%A"

echo Launching Zwift from: "%ZWIFT_EXECUTABLE_PATH%"

REM === 3. Start Zwift ===
start "" "%ZWIFT_EXECUTABLE_PATH%"

REM === 4. Wait for ZwiftApp.exe to start ===
echo Waiting for Zwift to start...
:wait_for_start
tasklist /FI "IMAGENAME eq ZwiftApp.exe" | find /I "ZwiftApp.exe" >nul
if errorlevel 1 (
    timeout /t 2 >nul
    goto wait_for_start
)

REM === 5. Wait for ZwiftApp.exe to close ===
echo Zwift is running... waiting for it to close.
:wait_for_exit
tasklist /FI "IMAGENAME eq ZwiftApp.exe" | find /I "ZwiftApp.exe" >nul
if not errorlevel 1 (
    timeout /t 5 >nul
    goto wait_for_exit
)

REM === 6. Ensure Windows venv exists and activate it ===
echo Zwift closed. Ensuring virtual environment exists...

set "VENV_PATH=%~dp0venv"
set "VENV_ACTIVATE=%VENV_PATH%\Scripts\activate.bat"
set "REQ_FILE=%~dp0requirements.txt"

REM Check if the venv exists
if not exist "%VENV_ACTIVATE%" (
    echo [INFO] Virtual environment not found. Creating one...
    py -m venv "%VENV_PATH%"
    
    if exist "%REQ_FILE%" (
        echo [INFO] Installing packages from requirements.txt...
        call "%VENV_ACTIVATE%"
        python -m pip install --upgrade pip >nul
        python -m pip install -r "%REQ_FILE%"
    ) else (
        echo [WARNING] No requirements.txt found at "%REQ_FILE%".
    )
)

REM Activate the venv (now it definitely exists)
call "%VENV_ACTIVATE%"

python main.py

endlocal
exit /b