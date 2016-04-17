# -*- coding: utf-8 -*-
from parsers import parser
import re

class amg(parser.parser):
    """
    Animagrad parser
    """
    def __init__(self):
        parser.parser.__init__(self)
        self.firstframe = True

    def do(self, data, mode):
        needcalc = False
        # activity
        f = re.findall(r'%s::(.*)' % status.ACTIVITY, data)
        if f:
            self.activity = f[0]
        # frame progress
        f = re.findall(r'%s::(\d+)' % status.PROGRESS, data)
        if f:
            needcalc = True
            self.percentframe = int(f[0])
        # error
        f = re.findall(r'%s::(.*)' % status.ERROR, data)
        if f:
            self.error = f[0]
            self.finishedsuccess = False
        # warning
        f = re.findall(r'%s::(.*)' % status.WARNING, data)
        if f:
            print (f[0])
        # compute
        if needcalc:
            self.calculate()


class status():
    ERROR       = 'ERROR'       # print error and stop process
    PROGRESS    = 'PROGRESS'    # progress in percent (0-100)
    ACTIVITY    = 'ACTIVITY'    # display activity on task
    MESSAGE     = 'MESSAGE'     # just print message
    WARNING     = 'WARNING'     # selected message as warning!!!
    FRAME       = 'FRAME'       # switch to next frame