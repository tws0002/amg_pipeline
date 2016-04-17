import os, json, re, subprocess

def server_is_started():
    root = os.getenv('AMG_ROOT')
    if not root:
        raise Exception('AMG Pipeline not defined!')
    tcping = os.path.join(os.path.dirname(__file__), 'bin', 'tcping.exe')

    if not all(serv.values()):
        return False
    cmd = '{tcping} -n 1 -w o.5 {host} {port}'.format(
        tcping=tcping,
        host=serv['server'],
        port=serv['port']
    )
    res = os.popen(cmd).read()
    if 'Port is open' in res:
        return True
    else:
        return False

def get_server_info():
    root = os.getenv('AMG_ROOT')
    conf1 = os.path.join(root, 'cgru', 'config.json').replace('\\','/')
    conf2 = os.path.join(root, 'cgru', 'afanasy', 'config_default.json').replace('\\','/')
    serv = dict(
        server=None,
        port=None
    )
    serv.update(get_server_config(conf2))
    serv.update(get_server_config(conf1))
    return serv

def get_server_config(path):
    conf = json.load(open(path))
    conf = conf.get('cgru_config')
    if not conf:
        return {}
    ret = {}
    if conf.get('af_servername'):
        ret['server'] = conf.get('af_servername')
    if conf.get('af_clientport'):
        ret['port'] = conf.get('af_clientport')
    return ret

def get_server_name_from_afcmd():
    if os.getenv('CGRU_LOCATION'):
        out = subprocess.check_output('/'.join([os.getenv('CGRU_LOCATION'),'afanasy/bin/afcmd']))
        find = re.findall(r"af_servername = '([\d.]+)'",out)
        return find[0]