@echo off
REM Run code quality checks

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Running Black formatter...
echo =========================
black modules/ scripts/

echo.
echo Running Flake8 linter...
echo =======================
flake8 modules/ scripts/

echo.
echo Running MyPy type checker...
echo ===========================
mypy modules/

echo.
echo Code quality checks complete!
echo.
pause