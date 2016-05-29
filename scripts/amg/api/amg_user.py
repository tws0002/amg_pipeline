import os, json
user_settings_file_name = 'amg_user_config.json'
import amg_path



class User(object):
    def __init__(self, username):
        self.username = username
        self.studio_path = amg_path.join(amg_path.ftp_path_users(), username)
        self.settings_file =  amg_path.join(self.studio_path, user_settings_file_name)
        data = self.settings()
        self.name = data['name']
        self.local_path = data['local_path']

    def __repr__(self):
        return 'AMG User (%s : %s)' % (self.username, self.name)

    def settings(self):
        if os.path.exists(self.settings_file):
            data = json.load(open(self.settings_file))
        else:
            data = dict(
                local_path='',
                name=self.username
            )
            json.dump(data, open(self.settings_file, 'w'), indent=2)
        return data

    def dict(self):
        s = self.settings()
        s['username'] = self.username
        s['studio_path'] = self.studio_path
        s['settings_file'] = self.settings_file
        return s

    def json(self):
        return json.dumps(self.dict(), indent=2)

def all_users():
    users_path = amg_path.ftp_path_users()
    users = []
    for u in os.listdir(users_path):
        if os.path.isdir(os.path.join(users_path, u)):
            usr = User(u)
            users.append(usr)
    return users
