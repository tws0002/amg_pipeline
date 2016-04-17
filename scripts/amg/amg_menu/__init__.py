import os, sys
amgroot = os.getenv('AMG_ROOT')
if amgroot:
    if not amgroot in sys.path:
        sys.path.append(amgroot)
    from amg_config import conf
    menu_name = conf.get('menu_title','AMG Tools')
else:
    menu_name = 'Tools'


def build_maya():
    # menus = [
    #     dict(
    #         title='',
    #         sources='',
    #         submenus=[]
    #     )
    # ]
    sources = [os.path.join(os.getenv('AMG_ROOT'), 'scripts', 'maya', 'python').replace('\\','/'),
               os.path.join(os.getenv('AMG_ROOT'), 'scripts', 'maya', 'mel').replace('\\','/')]
    env_sources = os.getenv('MENU_MAYA_SOURCES')
    if env_sources:
        sources += [x.replace('\\','/') for x in env_sources.split(os.pathsep)]

    from . import maya_menu
    reload(maya_menu)
    maya_menu.startBuild(menu_name, sources)


def build_nuke():
    sources = [os.path.join(os.getenv('AMG_ROOT'), 'scripts', 'nuke', 'python').replace('\\','/')]
    env_sources = os.getenv('MENU_NUKE_SOURCES')
    if env_sources:
        sources += [x.replace('\\','/') for x in env_sources.split(os.pathsep)]
    from . import nuke_menu
    nuke_menu.startBuild(menu_name, sources)

def build_mari():
    pass

def build_houdini():
    pass

def build_mbuilder():
    pass