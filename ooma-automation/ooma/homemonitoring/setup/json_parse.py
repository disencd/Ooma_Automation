import json

class JsonConfig():
    #Reading the config file from Json File
    def dump_config(self, filename):
        with open(filename) as json_data_file:
            data = json.load(json_data_file)
            return data