import json
from collections import OrderedDict
class JsonConfig():
    #Reading the config file from Json File
    def dump_config(self, filename):
        with open(filename) as json_data_file:
            data = json.load(json_data_file, object_pairs_hook=OrderedDict)
            return data