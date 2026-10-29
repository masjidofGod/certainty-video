@echo off
rem The kit's one command on Windows (Command Prompt and PowerShell). `certainty` alone lists what it does.
rem It finds Python 3.12 or 3.13 and hands over to engine\launch.py, which keeps the kit's packages ready.
setlocal
for %%V in (3.12 3.13) do (
  py -%%V -c "" >nul 2>nul
  if not errorlevel 1 (
    py -%%V -I "%~dp0..\engine\launch.py" %*
    exit /b
  )
)
python -c "import sys; sys.exit(0 if sys.version_info[:2] in ((3, 12), (3, 13)) else 1)" >nul 2>nul
if not errorlevel 1 (
  python -I "%~dp0..\engine\launch.py" %*
  exit /b
)
echo certainty needs Python 3.12 or 3.13: winget install --id Python.Python.3.12, then open a new terminal.
exit /b 1
