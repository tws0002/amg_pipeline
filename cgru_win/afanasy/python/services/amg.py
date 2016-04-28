# import amg service
import sys, os
amg_root = os.environ.get('AMG_ROOT')
amg_af = os.path.join(amg_root, 'scripts','amg','af').replace('\\','/')
if not amg_af in sys.path:
    sys.path.append(amg_af)
from amg_service import *