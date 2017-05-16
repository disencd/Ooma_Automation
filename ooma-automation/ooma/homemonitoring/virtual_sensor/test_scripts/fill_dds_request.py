from field_generator import FieldGenerator, DeviceDiscoveryGenerator

class DDS_data():
    def __init__(self):
        self.dd_gen = DeviceDiscoveryGenerator()

    def fill_deviceidentifier(self, sensor, iface):
        if sensor == "door":
            device_identifier = self.dd_gen.generate_door_deviceIdentifier(iface)
        elif sensor == "motion":
            device_identifier = self.dd_gen.generate_motion_deviceIdentifier(iface)
        elif sensor == "water":
            device_identifier = self.dd_gen.generate_water_deviceIdentifier(iface)

        return device_identifier

    def fill_dds_data(self, sensor_type):


        dds_request = {
            "libraryName": "OpenRemote Object Model",
            "javaFullClassName": "org.openremote.model.DeviceDiscovery",
            "schemaVersion": "2.0.0",
            "apiVersion": "0.2",
            "model": {
                "devices": [
                    {
                        "deviceIdentifier": self.fill_deviceidentifier(sensor_type, "BatteryIndicator-U1"),
                        "deviceName": "Battery Indicator",
                        "deviceProtocol": "ooma_ule",
                        "deviceModel": "BatteryIndicator",
                        "deviceType": "BatteryIndicator",
                        "deviceAttributes": {
                            "rootId": self.dd_gen.generate_rootId(),
                            "deviceId": self.dd_gen.generate_deviceId("U0S1I272"),
                            "unitId": "U1",
                            "interfaceType": "output",
                            "deviceType": "interface"
                        }
                    },
                    {
                        "deviceIdentifier": self.fill_deviceidentifier(sensor_type, "Alert-U1"),
                        "deviceName": "Alert",
                        "deviceProtocol": "ooma_ule",
                        "deviceModel": "Alert",
                        "deviceType": "Alert",
                        "deviceAttributes": {
                            "rootId": self.dd_gen.generate_rootId(),
                            "deviceId": self.dd_gen.generate_deviceId("U1S1I256"),
                            "unitId": "U1",
                            "interfaceType": "output",
                            "deviceType": "interface"
                        }
                    },
                    {
                        "deviceIdentifier": self.fill_deviceidentifier(sensor_type, "Announcement-U1"),
                        "deviceName": "Announcement",
                        "deviceProtocol": "ooma_ule",
                        "deviceModel": "Announcement",
                        "deviceType": "Announcement",
                        "deviceAttributes": {
                            "rootId": self.dd_gen.generate_rootId(),
                            "deviceId": self.dd_gen.generate_deviceId("U0S1I342458093"),
                            "unitId": "U1",
                            "interfaceType": "output",
                            "deviceType": "interface"
                        }
                    },
                    {
                        "deviceIdentifier": self.fill_deviceidentifier(sensor_type, "IdentifyDevice-U1"),
                        "deviceName": "Identify Device",
                        "deviceProtocol": "ooma_ule",
                        "deviceModel": "IdentifyDevice",
                        "deviceType": "IdentifyDevice",
                        "deviceAttributes": {
                            "rootId": self.dd_gen.generate_rootId(),
                            "deviceId": self.dd_gen.generate_deviceId("U0S1I4"),
                            "unitId": "U1",
                            "interfaceType": "output",
                            "deviceType": "interface"
                        }
                    },
                    {
                        "deviceIdentifier": self.fill_deviceidentifier(sensor_type, "TamperDetector-U1"),
                        "deviceName": "TamperDetector",
                        "deviceProtocol": "ooma_ule",
                        "deviceModel": "TamperDetector",
                        "deviceType": "TamperDetector",
                        "deviceAttributes": {
                            "rootId": self.dd_gen.generate_rootId(),
                            "deviceId": self.dd_gen.generate_deviceId("U0S1I257"),
                            "unitId": "U1",
                            "interfaceType": "output",
                            "deviceType": "interface"
                        }
                    },
                    {
                        "deviceIdentifier": self.fill_deviceidentifier(sensor_type, "UnregisterDevice-U1"),
                        "deviceName": "Unregister Device",
                        "deviceProtocol": "ooma_ule",
                        "deviceModel": "UnregisterDevice",
                        "deviceType": "UnregisterDevice",
                        "deviceAttributes": {
                            "rootId": self.dd_gen.generate_rootId(),
                            "deviceId": self.dd_gen.generate_deviceId("U0S1I342458094"),
                            "unitId": "U1",
                            "interfaceType": "output",
                            "deviceType": "interface"
                        }
                    },
                    {
                        "deviceIdentifier": self.fill_deviceidentifier(sensor_type, "ActiveDevice-U1"),
                        "deviceName": "Active Device",
                        "deviceProtocol": "ooma_ule",
                        "deviceModel": "ActiveDevice",
                        "deviceType": "ActiveDevice",
                        "deviceAttributes": {
                            "rootId": self.dd_gen.generate_rootId(),
                            "deviceId": self.dd_gen.generate_deviceId("U0S1I277"),
                            "unitId": "U1",
                            "interfaceType": "output",
                            "deviceType": "interface"
                        }
                    },
                    {
                        "deviceIdentifier": self.fill_deviceidentifier(sensor_type, "Window Sensor-root"),
                        "deviceName": "Window Sensor",
                        "deviceProtocol": "ooma_ule",
                        "deviceModel": "Window Sensor",
                        "deviceType": "Window Sensor",
                        "deviceAttributes": {
                            "Battery Rated Voltage (mV)": "3000",
                            "Friendly Name": "Window Sensor",
                            "deviceId": self.dd_gen.generate_rootId(),
                            "Battery Rated Capacity (mAHr)": "1050",
                            "Software Version": "187135",
                            "Battery Number of Cells": "2",
                            "Response Time": "0",
                            "Battery Manufacturer": "CHARGER MONSTER",
                            "Battery Maximum Voltage (mV)": "2800",
                            "Hardware Version": "dhx91-ooma-c",
                            "Battery Voltage (mV)": "2900",
                            "deviceType": "root",
                            "Battery Minimum Voltage (mV)": "2600",
                            "Manufacturer": "Ooma"
                        }
                    },
                    {
                        "deviceIdentifier": self.fill_deviceidentifier(sensor_type, "IdentifyInputDevice-U1"),
                        "deviceName": "Identify Input Device",
                        "deviceProtocol": "ooma_ule",
                        "deviceModel": "IdentifyInputDevice",
                        "deviceType": "IdentifyInputDevice",
                        "deviceAttributes": {
                            "rootId": self.dd_gen.generate_rootId(),
                            "deviceId": self.dd_gen.generate_deviceId("U0S1I342458095"),
                            "unitId": "U1",
                            "interfaceType": "output",
                            "deviceType": "interface"
                        }
                    },
                    {
                        "deviceIdentifier": self.fill_deviceidentifier(sensor_type, "RSSI128-U1"),
                        "deviceName": "RSSI biased +128",
                        "deviceProtocol": "ooma_ule",
                        "deviceModel": "RSSI+128",
                        "deviceType": "RSSI+128",
                        "deviceAttributes": {
                            "rootId": self.dd_gen.generate_rootId(),
                            "deviceId": self.dd_gen.generate_deviceId("1U0S1I273"),
                            "unitId": "U1",
                            "interfaceType": "output",
                            "deviceType": "interface"
                        }
                    }
                ]
            }
        }

        return dds_request

obj = DDS_data()