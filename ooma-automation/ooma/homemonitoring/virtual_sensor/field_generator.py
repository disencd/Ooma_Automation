import time, datetime

class FieldGenerator():
    def __init__(self):
        self.cust_pk = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        self.std_id = 20000

    #Customer PK - vn5j9av6ru7hjue7fpzek3r73m4ec8mq
    def generate_pk(self):
        self.cust_pk = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        return "virtualaccount" + str(self.cust_pk)

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
        return datetime.datetime.now().strftime("%M%S%f")


    #timezone - "America/Los_Angeles"
    def generate_timezone(self):
        return "America/Los_Angeles"

class DeviceDiscoveryGenerator():
    def __init__(self):
        # time.now().strftime("%M%S%f")
        # 1524559582
        #self.unique_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.unique_id = datetime.datetime.now().strftime("%M%S%f")

    def generate_uniqueID_for_sensor(self):
        self.unique_id = datetime.datetime.now().strftime("%M%S%f")

    #rootId - 1524559582
    def generate_rootId(self):
        return str(self.unique_id)

    #deviceIdentifier - 1524559582-Alert-U1
    def generate_deviceIdentifier(self, interface):
        return str(self.unique_id) + interface

    #"deviceId": "D1U0S1I4"
    def generate_deviceId(self, cnt, std_id):
        return "D" + str(cnt) + std_id
