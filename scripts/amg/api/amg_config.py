import os, json

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
default_conf = os.path.join(root, 'amg_config_example.json')
custom_conf = os.path.join(root, 'amg_config.json')

def get():
    data = json.load(open(default_conf))
    if os.path.exists(custom_conf):
        try:
            custom_data = json.load(open(custom_conf))
            data.update(custom_data)
        except:
            print 'Error syntas of custon config file'
    return data