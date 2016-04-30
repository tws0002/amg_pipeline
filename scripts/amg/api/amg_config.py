import os, json
import amg_user
root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
default_conf = os.path.normpath(os.path.join(root, 'amg_config_example.json'))
custom_conf  = os.path.normpath(os.path.join(root, 'amg_config.json'))
user_config  = os.path.normpath(os.path.join(root, amg_user.user_settings_file_name))

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

def get_user_config():
    if not os.path.exists(user_config):
        raise Exception('Cant found any config file')
    try:
        return json.load(open(user_config))
    except:
        raise Exception('Error syntax of user config file')

conf = get()
uconf = get_user_config()
