@echo off
setlocal enabledelayedexpansion

:: Set the path to your Python executable
set PYTHON_EXE=python.exe

:: Set the name of your Python script
set PYTHON_SCRIPT=aa11527_timingsimulator.py

:: Iterate over each subdirectory in the current directory
for /d %%i in (".\*") do (
    echo Processing directory: %%~nxi
    "%PYTHON_EXE%" "%PYTHON_SCRIPT%" --iodir "%%i"
)

echo Done processing all directories.
pause
