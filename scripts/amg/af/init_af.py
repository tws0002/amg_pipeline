import os, sys, json, subprocess

def init_af(CGRU_LOCATION):
    CGRU_LOCATION = CGRU_LOCATION.replace('\\','/').strip('/')
    if os.getenv('CGRU_LOCATION'):
        return
    os.environ['CGRU_LOCATION']= CGRU_LOCATION
    AF_PYTHON='/'.join([CGRU_LOCATION,'afanasy/python'])
    AF_BIN='/'.join([CGRU_LOCATION,'afanasy/bin'])
    CGRU_PYTHON='/'.join([CGRU_LOCATION,'lib/python'])

    os.environ['PYTHONPATH']=os.pathsep.join([AF_PYTHON, os.environ.get('PYTHONPATH','')])
    os.environ['PYTHONPATH']=os.pathsep.join([CGRU_PYTHON, os.environ.get('PYTHONPATH','')])
    sys.path.append(AF_PYTHON)
    sys.path.append(CGRU_PYTHON)
    sys.path.append(AF_BIN)