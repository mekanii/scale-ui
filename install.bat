@echo off
echo Installing Scale-UI project dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install dependencies. Please check the error messages above.
    exit /b %errorlevel%
)
echo Dependencies installed successfully.
PAUSE