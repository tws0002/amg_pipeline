import nuke
import collector
reload(collector)


def startBuild(menu_name, sources):
    data = collector.collectFilesData(menu_name, sources)
    data = collector.fixDuplicates(data)
    collector.printData(data)
    parent = nuke.menu("Nuke")
    # clear
    parent.removeItem(menu_name)
    #fill
    pw = addMenu(data, parent, True)
    if pw:
        pw.addSeparator()
        reloadMenu = 'from pw_nukeMenuGenerator import menuGenerator as mg;reload(mg);mg.startBuild()'
        pw.addCommand('Reload', reloadMenu)
        print 'MENU LOADED!!!'

def addMenu(data, parent, root=False):
    if data['type'] == 'sub' and 'content' in data:
        #create Menu
        sub = parent.addMenu(data['name'])
        #sort items
        menus = []
        actions = []
        for m in data['content']:
            if m['type'] == 'sub':
                menus.append(m)
            elif m['type'] == 'act':
                actions.append(m)
        menus = sorted(menus, key=lambda x:x['name'])
        actions = sorted(actions, key=lambda x:x['name'])

        #build
        for m in menus+actions:
            if m['type'] == 'sub':
                addMenu(m, sub)
            elif m['type'] == 'act':
                addItem(m, sub)
        return sub

def addItem(item, parent):
    #for python
    cmd = r'import '+item['module']+';reload('+item['module']+');'+item['module']+'.'+item['action']
    doc = item.get('doc','').strip().replace('\r','')
    action = parent.addCommand( name=item['name'], command=str(cmd), tooltip=doc )