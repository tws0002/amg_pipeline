import os, sys

#menuExample = [{'name':'UV', 'type':'sub', 'content':[
#                            {'name':'scriptName1', 'type':'act', 'cmd':'import module;reload(modele);module.go()'},
#                            {'name':'scriptName2', 'type':'mel', 'cmd':'source("filepath.mel");proc();'},
#                            {'name':'scriptFolder', 'type':'sub', 'content':[]}
#                                              ]
#        }]
###data example
'''menuData
sub=SimpleModMenu
    act={name:Action1,action:show()}
    act={name:Action2,action:show1(),option:help()}
act={name:Action3,action:show2()}
sub=SimpleSubMenu2
    act={name:DoIt4,action:show3()}
'''
'''moduleInfo
Its module for test
'''

init = '__init__.py'

############################## COLLECT FILE DATA
#return dict
def collectFilesData(label, sources):
    data = {'name':label, 'type':'sub','content':[]}
    for scriptPath in sources:
        if os.path.exists(scriptPath):
            addPYTHONPATH(scriptPath)
            d = folderIter(scriptPath) #return list
            if d:
                data['content'] += d
        else:
            print 'Error path', scriptPath
    return fixDuplicates(data)

def printData(data, ind = ''):
    print ind, data['name']#,
    if 'content' in data and data['type'] == 'sub':
        ind += '   '
        for s in data['content']:
            printData(s, ind)

def folderIter(folder):
    actions = []
    files = os.listdir(folder)
    for f in files:
        fullPath = os.path.join(folder, f)
        #if file
        if os.path.isfile(fullPath):
            if os.path.splitext(fullPath)[-1].lower() == '.py' and not f == init:
                d = readFile(fullPath) # return list of actions \ menu
                if d:
                    addPYTHONPATH(os.path.dirname(fullPath))
                    actions += d
            elif os.path.splitext(fullPath)[-1].lower() == '.mel':
                d = readFile(fullPath, True) #read list of actions \ menu
                if d:
                    actions += d
        #if dir
        elif os.path.isdir(fullPath):
            if init in os.listdir(fullPath):#is package
                d = readFile(os.path.join(fullPath, init)) #return actions in package
                if d:
                    actions += d
            else:
                d = folderIter(fullPath) # return inside list of actions\menu
                if d:
                    addPYTHONPATH(fullPath)
                    actions.append({'name':f, 'type':'sub', 'content':d})
    return actions

def readFile(path, MEL=False):
    lines, doc = readLines(path, MEL)
    data = parseLines(lines, MEL, doc)
    d = completeData(data, path, MEL)
    return d

def completeData(data,  path, MEL):

    for act in data:
        #add imported module
        if os.path.basename(path) == init: #is package
            act['module'] = os.path.basename(os.path.dirname(path))
        elif MEL == True: #is MEL
            act['module'] = path.replace('\\','/')
        else: #is module
            act['module'] = os.path.splitext(os.path.basename(path))[0]
        if act['type'] == 'sub':
            act['content'] = completeData(act['content'], path, MEL)
    return data

def readLines(path, ml=False):
    lines = []
    doc = ''

    commentStr = {True:"/*", False:"'''"}
    commentEnd = {True:"*/", False:"'''"}

    f = open(path, 'r')
    if f:
        if not commentStr[ml]+"menuData" in f.readline():
            f.close()
            return lines, doc
        for line in iter(f.readline, ''):
            if commentEnd[ml] in line or not line.strip():
                break
            lines.append(line.replace('\n', ''))

        #find info
        if not commentStr[ml]+"moduleInfo" in f.readline():
            f.close()
            return lines, doc
        for line in iter(f.readline, ''):
            if commentEnd[ml] in line or not line.strip():
                break
            doc += line
    f.close()
    return lines, doc

######## parse
def parseLines(lines, MEL, doc, ind=0):
    actions = []
    actType = {True:'mel', False:'act'}
    while lines:
        line = lines.pop(0)
        ofs = '    '*ind
        if line.startswith(ofs+'act'):
            data = line.split('{')[-1].split('}')[0].split(',')
            act = {}
            for d in data:
                act[d.split(':')[0]] = d.split(':')[1]
            act['type'] = actType[MEL]
            act['doc'] = doc
            actions.append(act)
        elif line.startswith(ofs+'sub'):
            subLines = []
            while True:
                if not lines:break
                if lines[0].startswith('    '*(ind+1)):
                    subLines.append(lines.pop(0)[4:])
                else:
                    break
            if subLines:
                content = parseLines(subLines, MEL, doc, ind)
                if content:
                    act = {'type':'sub',
                           'content':content,
                           'name':line.strip().split('=')[-1]}
                    actions.append(act)
    return actions

def fixDuplicates(data):
    currentLevel = []
    newData = []
    cont = data['content']
    for d in cont:
        if d['type'] == 'sub':
            currentLevel.append(d['name'])
    if not len(currentLevel) == len(list(set(currentLevel))):
        while cont:
            next = cont.pop(0)
            if currentLevel.count(next['name'])>1:
                for c in cont:
                    if c['name'] == next['name']:
                        next['content']+=c['content']
                        cont.pop(cont.index(c))
            newData.append(next)

        for c in newData:
            if c['type'] == 'sub':
                c = fixDuplicates(c)
        data['content'] = newData
    return data

def addPYTHONPATH(path):
    path = path.replace('\\','/')
    if not path in sys.path:
        sys.path.append(path)