rem amgenv
@echo off
PUSHD ..
IF NOT DEFINED AMG_ROOT (
	call amg_env.cmd
)
rem tray icon
start %AMG_ROOT%\python\python.exe amg_launcher\tray_icon.py
rem afrender
set PYTHONHOME=
REM TODO replace to afrender monitor
start %AMG_ROOT%\cgru\start\AFANASY\render.cmd
rem shotgun
start %AMG_ROOT%\python\pythonw.exe %AMG_ROOT%\start\amg_start_shotgun.py
POPD