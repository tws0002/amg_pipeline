rem render node startup script
@echo off
PUSHD ..
set PATH=%cd%;%cd%\scripts;%PATH%
set PYTHONHOME=
call %AMG_ROOT%\cgru\start\AFANASY\render.cmd
POPD