import nuke, os, sys
from amg import icons

nuke.tprint('============== init.py is running\n')

# nuke root
NUKE_PATH = os.path.join(os.getenv('AMG_ROOT'), 'scripts', 'nuke')

#add plugin path
nuke.pluginAddPath(os.path.join(NUKE_PATH, 'gizmos').replace('\\','/'))
nuke.pluginAddPath(os.path.join(NUKE_PATH, 'icons').replace('\\','/'))
nuke.pluginAddPath(os.path.join(os.getenv('AMG_PLUGINS'), 'nuke'))

# python
os.environ['PYTHONPATH'] = os.path.join(NUKE_PATH, 'python')

#favorites

nuke.addFavoriteDir( 'AMG', '[getenv AMG_ROOT]', nuke.IMAGE | nuke.GEO | nuke.FONT | nuke.PYTHON, icon=icons.ico['animagrad'] )


