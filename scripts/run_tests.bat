@echo off
REM Run tests for all modules

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Running tests for PDF to Markdown module...
echo ==========================================
pytest modules/pdf_to_markdown/tests/ -v --tb=short

echo.
echo Running all module tests with coverage...
echo =========================================
pytest modules/ -v --tb=short --cov=modules --cov-report=html --cov-report=term

echo.
echo Test results complete!
echo Coverage report saved to htmlcov/index.html
echo.
pause