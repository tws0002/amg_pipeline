@echo off
PUSHD ..
IF NOT DEFINED AMG_ROOT (
	call amg_env.cmd
)
set PATH=%cd%;%cd%\scripts;%PATH%
set PYTHONPATH=%cd%;%cd%\scripts
start %cd%\python\pythonw.exe %AMG_UTIL%\amg_scene_packer\packer_window.py
POPD