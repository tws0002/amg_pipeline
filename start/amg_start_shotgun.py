import subprocess, os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import amg_config

sh_path = amg_config.conf.get('shotgun_exe')
if sh_path:
    if os.path.exists(sh_path):
        subprocess.Popen(sh_path)
    else:
        print 'ERROR: File not found %s' % sh_path
else:
    print 'ERROR: path not set'