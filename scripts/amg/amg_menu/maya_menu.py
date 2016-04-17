import maya.cmds as cmds
from maya import mel
import collector
reload(collector)


def startBuild(menu_name, sources):
    # print '-'*50
    data = collector.collectFilesData(menu_name, sources)
    maya = mel.eval('$temp=$gMainWindow')
    name = menu_name.lower().replace(' ','_')
    # print name
    # print '-'*50
    if cmds.menu(name, exists=1):
        cmds.deleteUI(name)
    menu = addMenu(data, maya, True, name)
    cmds.menuItem( divider=True, p=menu )
    #reloadMenu = 'import maya.mel as mel;mel.eval("rehash;source userSetup;")'
    if not menu_name and not sources:
        reloadMenu = 'from amg import amg_menu;reload(amg_menu);amg_menu.build_maya()'
    else:
        reloadMenu = 'from amg import amg_menu;reload(amg_menu);amg_menu.build_maya("%s", %s)' % (menu_name, str(sources))

    cmds.menuItem( label='Reload menu', c=reloadMenu, p=menu)
    print 'MENU %s LOADED!!!' % name



def addMenu(data, parent, root=False, menu_name=None):
    if data['type'] == 'sub' and 'content' in data:
        #create Menu
        if root:
            sub = cmds.menu(menu_name, label=data['name'], tearOff=True, p=parent )
        else:
            sub = cmds.menuItem(label=data['name'], tearOff=True, subMenu=True, p=parent)
        #sort items
        menus = []
        actions = []
        for m in data['content']:
            if m['type'] == 'sub':
                menus.append(m)
            elif m['type'] in ['act', 'mel']:
                actions.append(m)
        menus = sorted(menus, key=lambda x:x['name'])
        actions = sorted(actions, key=lambda x:x['name'])

        #build
        #for m in data['content']:
        for m in menus+actions:
            if m['type'] == 'sub':
                addMenu(m, sub)
            elif m['type'] == 'act' or m['type'] == 'mel':
                addItem(m, sub)
        return sub

def addItem(item, parent):
    #for python
    if item['type'] == 'act':
        cmd = r'import '+item['module']+';reload('+item['module']+');'+item['module']+'.'+item['action']
        if not 'option' in item:
            if item['doc']:
                doc = item['doc'].strip().replace('\r','')
                opt = 'import maya.cmds;maya.cmds.confirmDialog(title="Help for: '+ item['name']+'" ,message="' + doc + '", button=["OK"], defaultButton="OK")'
            else:
                opt = ''
        else:
            opt = 'import '+item['module']+';reload('+item['module']+');'+item['module']+'.'+item['option']
    #for mel
    elif item['type'] == 'mel':
        cmd = 'import maya.mel;maya.mel.eval(\'source "'+item['module']+'";'+item['action']+'\')'
        if not 'option' in item:
            if item['doc']:
                doc = item['doc'].strip().replace('\r','')
                opt = 'import maya.mel;maya.mel.eval(\'confirmDialog -title "Help for: '+item['name']+'" -message "'+doc+'" -button "OK" -defaultButton "OK";\')'
            else:
                opt = ''
        else:
            opt = "import maya.mel;maya.mel.eval("+item['option']+'")'
    opt = opt.replace('\n', '\\n')


    action = cmds.menuItem( label=item['name'], command=cmd, p=parent )
    if opt:
        cmds.menuItem( optionBox=True, command=opt, p=parent )
