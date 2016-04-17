@echo off
rem AMG evns for afanasy

set AMG_ROOT=%~dp0
IF %AMG_ROOT:~-1%==\ SET AMG_ROOT=%AMG_ROOT:~0,-1%
rem utils
set AMG_UTIL=%AMG_ROOT%\scripts\amg\utils
rem plugins
set AMG_PLUGINS=%AMG_ROOT%\plugins
rem scripts
set PATH=%AMG_ROOT%;%AMG_ROOT%\scripts\amg\af\bin;%AMG_ROOT%\scripts;%PATH%

rem Call custom setup scripts named "env_*.cmd" :
For /F "Tokens=*" %%I in ('dir /b env_*.cmd') Do call %%I
