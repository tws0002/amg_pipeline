import os

icons = {os.path.splitext(x)[0]: os.path.join(os.path.dirname(__file__),x).replace('\\','/') for x in  os.listdir(os.path.dirname(__file__)) if os.path.splitext(x)[-1] == '.png'}