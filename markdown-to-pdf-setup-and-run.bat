@echo off
setlocal enabledelayedexpansion

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python and try again.
    pause
    exit /b 1
)

:: Check and install required libraries
set "libraries=markdown pdfkit PyPDF2"
for %%i in (%libraries%) do (
    python -c "import %%i" >nul 2>&1
    if !errorlevel! neq 0 (
        echo Installing %%i...
        pip install %%i
        if !errorlevel! neq 0 (
            echo Failed to install %%i. Please install it manually.
            pause
            exit /b 1
        )
    )
)

:: Check if wkhtmltopdf is installed
wkhtmltopdf --version >nul 2>&1
if %errorlevel% neq 0 (
    echo wkhtmltopdf is not installed.
    echo Please download and install it from https://wkhtmltopdf.org/downloads.html
    echo After installation, add the wkhtmltopdf bin directory to your system PATH.
    pause
    exit /b 1
)

:: Run the Python script
echo Running Markdown to PDF converter...
python markdown_to_pdf.py

if %errorlevel% neq 0 (
    echo An error occurred while running the script.
    pause
    exit /b 1
)

echo Conversion completed successfully.
pause
