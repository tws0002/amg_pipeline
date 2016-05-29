import os

root = os.path.join(os.path.dirname(__file__), 'icons')

ico = dict(
    animagrad=os.path.join(root, 'animagrad.png').replace('\\','/'),
    shotgun=os.path.join(root, 'shotgun.png').replace('\\','/'),
    maya=os.path.join(root, 'maya.png').replace('\\','/'),
    max=os.path.join(root, 'max.png').replace('\\','/'),
    nuke=os.path.join(root, 'nuke.png').replace('\\','/'),
    houdini=os.path.join(root, 'houdini.jpg').replace('\\','/'),
    image=os.path.join(root, 'image.png').replace('\\','/'),
    text=os.path.join(root, 'text.png').replace('\\','/'),
    arnold=os.path.join(root, 'arnold.png').replace('\\','/'),
    clock=os.path.join(root, 'wait.png').replace('\\','/'),
    other=os.path.join(root, 'other.png').replace('\\','/')
)

extico = dict(
    default=  ico['other'],
    ma=       ico['maya'],
    mb=       ico['maya'],
    max=      ico['max'],
    hip=      ico['houdini'],
    nk=       ico['nuke'],
    tif=      ico['image'],
    tiff=     ico['image'],
    jpg=      ico['image'],
    jpeg=     ico['image'],
    tx=       ico['arnold'],
    ass=      ico['arnold'],
    txt=      ico['text'],
    doc=      ico['text'],
    docx=     ico['text']
)
