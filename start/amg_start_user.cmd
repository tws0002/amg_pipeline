rem outsource users startup script
PUSHD ..
IF NOT DEFINED AMG_ROOT (
	call amg_env.cmd
)
call %AMG_ROOT%\python\python.exe