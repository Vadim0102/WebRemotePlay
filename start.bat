@echo off
setlocal

rem Check for Python 3
python --version 2>NUL | findstr /R /C:"^Python 3" >NUL
if errorlevel 1 (
    echo Python 3 is not installed.
    exit /b 1
)

rem Check for main.py file
if not exist "main.py" (
    echo main.py file not found.
    exit /b 1
)

rem Check for venv environment
if not exist "venv\" (
    echo Virtual environment not found. Creating environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error creating virtual environment.
        exit /b 1
    )
)

rem Activate virtual environment
call venv\Scripts\activate

rem Check for requirements.txt file and install modules
if exist "requirements.txt" (
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error installing modules from requirements.txt.
        exit /b 1
    )
) else (
    echo requirements.txt file not found. Skipping module installation.
)

rem Run main.py script
cls
python main.py
if errorlevel 1 (
    echo Error running main.py script.
    exit /b 1
)

endlocal
exit /b 0
