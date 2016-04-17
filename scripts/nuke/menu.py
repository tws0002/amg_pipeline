import nuke, os
from amg import icons

nuke.tprint('============== menu.py is running\n')
nuke_path = os.getenv('NUKE_PATH').split(';')[0]
#My custom formats
# nuke.addFormat ('1280 720 1.0 720p')

#Nuke defaults
nuke.knobDefault('Root.format', '720p')

toolbar = nuke.toolbar("Nodes") # Access the main toolbar
menubar = nuke.menu("Nuke") # Access the main menu bar

def initGizmos():
    allgizmos = toolbar.addMenu('all_gizmos', icon=icons.ico['animagrad'])
    gizmos = os.path.join(nuke_path, 'gizmos').replace('\\','/')
    nuke.tprint('============== CUSTOM GIZMOS: %s' % gizmos)
    for d, dirs, files in os.walk(gizmos):
        for file in files:
            gizmo_name, ext = os.path.splitext(file)
            if ext == '.gizmo':
                allgizmos.addCommand(gizmo_name, "nuke.createNode(\"" + gizmo_name + '\")' )
                nuke.tprint(gizmo_name)
    nuke.tprint('==============')

initGizmos()