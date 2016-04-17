import os, json, copy

root = os.path.dirname(__file__)
config_file = os.path.join(root, 'amg_config_example.json')
config_file_overwrite = os.path.join(root, 'amg_config.json')
if not os.path.exists(config_file):
    raise Exception('AMG Config not found')
conf_orig = json.load(open(config_file))

if os.path.exists(config_file_overwrite):
    over = json.load(open(config_file_overwrite))
    conf = copy.deepcopy(conf_orig)
    conf.update(over)
else:
    conf = conf_orig