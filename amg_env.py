import os, glob, sys

root = os.path.dirname(__file__)
from amg_config import conf, conf_orig


def amg_env():
    # AMG_ROOT
    os.environ['AMG_ROOT'] = root
    # AMG_PLUGINS
    os.environ['AMG_PLUGINS'] = join(root, 'plugins')
    # AMG_TEMP
    if not os.path.exists(conf['tmp_dir']):
        try:
            os.makedirs(conf['tmp_dir'])
            os.environ['AMG_TEMP'] = conf['tmp_dir']
        except:
            os.environ['AMG_TEMP'] = conf_orig['tmp_dir']
    else:
        os.environ['AMG_TEMP'] = conf['tmp_dir']
    # PATH
    scriptspath = join(root, 'scripts')
    addEnv(scriptspath, 'PYTHONPATH')
    if not scriptspath in sys.path:
        sys.path.insert(0, scriptspath)
    # CUSTOM
    if conf.get('load_custom_py'):
        import_custom()

def maya_env():
    amg_env()
    from amg.af import init_af
    # define maya env
    addEnv(join(root, 'scripts', 'maya', 'python'), 'PYTHONPATH')
    addEnv(join(root, 'scripts', 'maya', 'mel'), 'MAYA_SCRIPT_PATH')
    addEnv(join(root, 'scripts', 'maya', 'icons'), 'XBMLANGPATH')
    addEnv(join(root, 'scripts', 'maya', 'shelves'),'MAYA_SHELF_PATH')
    # CGRU
    CGRU_LOCATION = join(root, 'cgru')
    init_af.init_af(CGRU_LOCATION)
    # CGRU MAYA
    MAYA_CGRU_LOCATION=join(CGRU_LOCATION,'plugins/maya')
    addEnv(MAYA_CGRU_LOCATION, 'MAYA_CGRU_LOCATION')
    addEnv(MAYA_CGRU_LOCATION, 'PYTHONPATH')
    addEnv(join(MAYA_CGRU_LOCATION, 'afanasy'), 'PYTHONPATH')
    addEnv('CGRU','MAYA_CGRU_MENUS_NAME')

        # addEnv(join(MAYA_CGRU_LOCATION, 'mel','AETemplates'), 'MAYA_SCRIPT_PATH')
        # addEnv(join(MAYA_CGRU_LOCATION,'mll', 'version'),'MAYA_PLUG_IN_PATH')
    # ARNOLD
    # todo: add Arnold env

def nuke_env():
    amg_env()
    from amg.af import init_af
    # define nuke
    addEnv(join(root, 'scripts', 'nuke'), 'NUKE_PATH')
    addEnv(join(root, 'scripts', 'nuke', 'python'), 'PYTHONPATH')


def houdini_env():
    amg_env()
    from amg.af import init_af
    # define houdini

####################################

def join(*args):
    return os.path.normpath(os.path.abspath(os.path.join(*[str(x) for x in args]))).replace('\\','/')

def addEnv(path, env):
    if not path in os.environ.get(env,'').split(os.pathsep):
        os.environ[env] = normEnv(os.pathsep.join([path, os.environ.get(env,'')]))

def normEnv(path):
    path =  os.pathsep.join([x for x in path.replace('\\','/').replace('//','/').split(os.pathsep) if x])
    return path

def import_custom():
    # add try import
    for script in glob.glob1(root, 'custom_*.py'):
        try:
            __import__(os.path.splitext(script)[0])
        except:
            print 'Error load module %s' % script
