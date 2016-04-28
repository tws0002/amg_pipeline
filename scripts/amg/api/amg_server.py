import amg_config
import time, hashlib, requests, types


class AMGServer(object):
    def __init__(self, url, username, password, token):
        # super(AMGServer, self).__init__()
        # todo Get next data from config
        self.__url = url
        self.__username = username
        self.__password = password
        self.__token = token

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
