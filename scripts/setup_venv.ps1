# Setup virtual environment for Python Utility Library

Write-Host "Creating virtual environment..." -ForegroundColor Green
python -m venv venv

Write-Host "Activating virtual environment..." -ForegroundColor Green
& "venv\Scripts\Activate.ps1"

Write-Host "Installing dependencies..." -ForegroundColor Green
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt

Write-Host "Installing project in development mode..." -ForegroundColor Green
pip install -e .

Write-Host ""
Write-Host "Setup complete! To activate the virtual environment, run:" -ForegroundColor Yellow
Write-Host "  venv\Scripts\Activate.ps1" -ForegroundColor Yellow
Write-Host ""