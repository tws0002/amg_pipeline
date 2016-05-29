import os, json
# from amg.api import amg_user
# root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
root = os.path.dirname(__file__)
default_conf = os.path.normpath(os.path.join(root, 'amg_config_example.json'))
custom_conf  = os.path.normpath(os.path.join(root, 'amg_config.json'))

def get():
    if os.path.exists(default_conf):
        data = json.load(open(default_conf))
        if os.path.exists(custom_conf):
            try:
                custom_data = json.load(open(custom_conf))
                data.update(custom_data)
            except:
                raise Exception('Error syntax of custom config file')
        return data
    else:
        raise Exception('Cant found any config file')

conf = get()
