@echo off
echo ===============================================
echo Building Detection System - Quick Setup
echo ===============================================

echo.
echo Setting up environment...
powershell -Command "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process"
python -m venv building
call building\Scripts\activate

echo.
echo Installing required packages...
pip install -r requirements.txt

echo.

echo.
echo Setup complete!
echo.
echo To run building detection:
echo   python building_detector.py
echo.
echo Or for GUI interface:
echo   python building_detector_gui.py
echo.
pause