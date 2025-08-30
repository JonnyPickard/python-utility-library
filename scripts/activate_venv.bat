@echo off
REM Activate virtual environment

if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
    echo Virtual environment activated!
    echo.
    echo Python location: %VIRTUAL_ENV%\Scripts\python.exe
    echo.
    cmd /k
) else (
    echo Virtual environment not found!
    echo Run setup_venv.bat first to create it.
    pause
)