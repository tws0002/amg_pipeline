import time, hashlib, requests
import amg_config
reload(amg_config)


class AMGServer(object):
    def __init__(self, url=None, username=None, password=None, token=None, port=None):
        # todo Get next data from config
        port = ((':%s' % (port or amg_config.conf['api_port'])) if (port or amg_config.conf['api_port']) else '')
        self.__url = 'http://' + (url or amg_config.conf['animagrad_url']) + port + '/' + amg_config.conf['api_url'].replace('\\','/').strip('/') + '/'
        self.__username = username or amg_config.conf['username']
        self.__password = password or amg_config.conf['password']
        self.__token = token or amg_config.conf['token']

    def api_path(self):
        return self.__url

    def __getattr__(self, command):
        def _call(*args, **kwargs):

            stamp = int(time.time())
            m = hashlib.md5()
            m.update("%s_%s" % (self.__token, stamp))
            code = m.hexdigest()
            data = dict(
                auth=dict(
                    username=self.__username,
                    password=self.__token,
                    timestamp=stamp,
                    hash=code
                    ),
                function=command,
                args=args,
                kwargs=kwargs
                )
            r = requests.post(self.__url, json=data)
            try:
                return r.json()
            except:
                return r.text
        return _call
