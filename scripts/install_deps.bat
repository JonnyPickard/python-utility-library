@echo off
REM Install or update dependencies

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Upgrading pip...
pip install --upgrade pip

echo Installing production dependencies...
pip install -r requirements.txt

echo Installing development dependencies...
pip install -r requirements-dev.txt

echo Installing project in development mode...
pip install -e .

echo.
echo Dependencies installed successfully!
echo.
pause