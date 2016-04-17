# -*- coding: utf-8 -*-
from services import service
import sys, re

parser = 'amg'
pyt = sys.executable

class amg(service.service):
    """
    Animagrad service
    """

    # def __init__(self, taskInfo, i_verbose):
    #     taskInfo['command'] = self.build_command(taskInfo['command'])
    #     super(amg, self).__init__(taskInfo, i_verbose)
    #
    # def build_command(self, cmd):
    #     if cmd.startswith('system '):
    #         s = re.search(r'system "?(.*)"?', cmd)
    #         if s:
    #             cmd = s.group(1)
    #             return cmd
    #         else:
    #             raise Exception('Wrong system command: %s' % cmd)
    #     else:
    #         return cmd