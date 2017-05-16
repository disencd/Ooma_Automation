import time, datetime

class FieldGenerator():
    def __init__(self):
        self.std_id = 11

    #Customer PK - vn5j9av6ru7hjue7fpzek3r73m4ec8mq
    def generate_pk(self):
        self.std_id = self.std_id + 1
        return "virtualsensors" + str(self.std_id).zfill(18)

    #orUsername - ui89dg3p4
    def generate_orUsername(self):
        return "Vir" + str(self.std_id).zfill(6)

    #orPassword - YmJoajlqaWJi
    def generate_orPassword(self):
        return "Vir" + str(self.std_id).zfill(9)

    #nimbitsUsername - sun2pfbjr@ooma.com
    def generate_nimbitsUsername(self):
        return "Vir" + str(self.std_id).zfill(6) + "@ooma.com"

    #nimbitsPassword - dmdlZmc3OWV2
    def generate_nimbitsPassword(self):
        return "Vir" + str(self.std_id).zfill(9)

    #spn - 9712732945
    def generate_SPN(self):
        return '1' + str(self.std_id).zfill(9)

    #timezone - "America/Los_Angeles"
    def generate_timezone(self):
        return "America/Los_Angeles"

class DeviceDiscoveryGenerator():
    def __init__(self):
        # time.now().strftime("%Y%m%d%H%M%S")
        # 20120515155045
        self.unique_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.cnt = 0

    #rootId - 20120515155045
    def generate_rootId(self):
        return str(self.unique_id)

    #deviceIdentifier - vw20120515155045-Alert-U1
    def generate_water_deviceIdentifier(self, interface):
        return "vw" + str(self.unique_id) + '-' + interface

    # deviceIdentifier - vd20120515155045-Alert-U1
    def generate_door_deviceIdentifier(self, interface):
        return "vd" + str(self.unique_id) + '-' + interface

    # deviceIdentifier - vm20120515155045-Alert-U1
    def generate_motion_deviceIdentifier(self, interface):
        return "vm" + str(self.unique_id) + '-' + interface

    #"deviceId": "D1U0S1I4"
    def generate_deviceId(self, std_id):
        return "D" + str(self.cnt) + std_id
