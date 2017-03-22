import json

from xlrd import open_workbook as OW


class JsonConfig():
    def dump_config(self):
        with open('../setup/oss_config.json') as json_data_file:
            data = json.load(json_data_file)
            return data

class excel_modification(JsonConfig):
    def __init__(self):
        self.wb = OW("blah1.csv")

    def modify_myxid(self, data):
        s = self.wb.get_sheet(0)
        s.write(0, 0, data["device_credentials"]["myxid"])
#print(data["cert"]["oss_url"])

