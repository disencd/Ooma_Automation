
class FieldGenerator():
    def __init__(self):
        self.std_id = 6

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
        self.std_id = 6

    #rootId - VirWaterrootId02e9e0009d1"
    def generate_water_rootId(self):
        self.std_id = self.std_id + 1
        return "VirWaterrootId" + str(self.std_id).zfill(6)

    # rootId - VirdoorrootId02e9e0009d1"
    def generate_door_rootId(self):
        self.std_id = self.std_id + 1
        return "VirDoorrootId" + str(self.std_id).zfill(6)

    # rootId - VirMotionrootId02e9e0009d1"
    def generate_motion_rootId(self):
        self.std_id = self.std_id + 1
        return "VirMotionrootId" + str(self.std_id).zfill(6)

    #deviceIdentifier - VirWater
    def generate_water_deviceIdentifier(self):
        return "VirWaterDiD" + str(self.std_id).zfill(6)

    # deviceIdentifier - VirDoor
    def generate_door_deviceIdentifier(self):
        return "VirDoorDiD" + str(self.std_id).zfill(6)

    # deviceIdentifier - VirMotion
    def generate_motion_deviceIdentifier(self):
        return "VirMotionDiD" + str(self.std_id).zfill(6)

    #deviceName - VirWater
    def generate_water_deviceName(self):
        return "VirWaterDname " + str(self.std_id).zfill(6)

    #deviceName - VirDoor
    def generate_door_deviceName(self):
        return "VirDoorDname " + str(self.std_id).zfill(6)

    #deviceName - VirMotion
    def generate_motion_deviceName(self):
        return "VirMotionDname " + str(self.std_id).zfill(6)

    #deviceModel - dectFloodDetector
    def generate_water_deviceModel(self):
        return "dectFloodDetector"

    #deviceModel - dectDoorDetector
    def generate_door_deviceModel(self):
        return "dectDoorDetector"

    #deviceModel - dectMotionDetector
    def generate_motion_deviceModel(self):
        return "dectMotionDetector"