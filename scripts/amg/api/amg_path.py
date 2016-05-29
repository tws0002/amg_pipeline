import os, subprocess
import amg_config

def ftp_path():
    conf = amg_config.get()
    return conf.get('ftp_path','').replace('\\','/')

def ftp_path_users():
    return os.path.join(ftp_path(),'users').replace('\\','/')

def studio_projects_path():
    conf = amg_config.get()
    return conf.get('projects_path','').replace('\\','/')

def join(*args):
    return '/'.join([str(x.replace('\\','/').rstrip('/')) for x in args])


def hide(path):
    if os.name == 'nt':
        cmd = 'attrib +h %s' % path.replace('/','\\')
        CREATE_NO_WINDOW = 0x08000000
        subprocess.call(cmd, creationflags=CREATE_NO_WINDOW)
