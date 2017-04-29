#!/usr/bin/python
import socket, sys

if len(sys.argv) < 2:
    print "Usage: script.py <data_to_send>"
    sys.exit(0)

#address = ("192.168.220.68", 4443)
address = ("localhost", 4443)
data = sys.argv[1]

print "Sending UDP packet with data '{}' to {}:{}".format(data, address[0], address[1])

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(data, address)



'''
Register Telo
./sendUdpPacket.py '@ "0000000000-device" "Telo Base Station" "dectBaseStation" "dectBaseStation" "deviceId":"0000000000" "deviceType":"root"'
./sendUdpPacket.py '@ "0000000000-AN" "Announcement" "Announcement" "Announcement" "deviceId":"AN" "deviceType":"interface" "rootId":"0000000000" "interfaceType":"output" "unitId":"U0" "unitName":"System"'
./sendUdpPacket.py '@ "0000000000-RN" "OomaBaseStationRegistration" "OomaBaseStationRegistration" "OomaBaseStationRegistration" "deviceId":"RN" "deviceType":"interface" "rootId":"0000000000" "interfaceType":"input" "unitId":"U1" "unitName":"Ooma Base Station Registration"'
./sendUdpPacket.py '@ "0000000000-RG" "OomaBaseStationRegistration" "OomaBaseStationRegistration" "OomaBaseStationRegistration" "deviceId":"RG" "deviceType":"interface" "rootId":"0000000000" "interfaceType":"output" "unitId":"U0" "unitName":"Ooma Base Station Registration"'
./sendUdpPacket.py '@ "0000000000-SK" "Active Device" "ActiveDevice" "ActiveDevice" "deviceId":"SK" "deviceType":"interface" "rootId":"0000000000" "interfaceType":"output" "unitId":"U0" "unitName":"System"'
./sendUdpPacket.py '@ "0000000000-SP4" "OomaBaseStationFlashFIRE" "OomaBaseStationFlashFIRE" "OomaBaseStationFlashFIRE" "deviceId":"SP4" "deviceType":"interface" "rootId":"0000000000" "interfaceType":"output" "unitId":"U4" "unitName":"Ooma Base Station Flash FIRE"'
./sendUdpPacket.py '@ "0000000000-SP3" "OomaBaseStationFlashRedBlue" "OomaBaseStationFlashRedBlue" "OomaBaseStationFlashRedBlue" "deviceId":"SP3" "deviceType":"interface" "rootId":"0000000000" "interfaceType":"output" "unitId":"U3" "unitName":"Ooma Base Station Flash Red/Blue"'

Register sensor
./sendUdpPacket.py '@ "02e9e0002e-U0S1I342458093" "Announcement" "Announcement" "Announcement" "deviceId":"D2U0S1I342458093" "deviceType":"interface" "rootId":"02e9e0002e" "interfaceType":"output" "unitId":"U1" '
./sendUdpPacket.py '@ "02e9e0002e-U0S1I342458094" "Unregister Device" "UnregisterDevice" "UnregisterDevice" "deviceId":"D2U0S1I342458094" "deviceType":"interface" "rootId":"02e9e0002e" "interfaceType":"output" "unitId":"U1" '
./sendUdpPacket.py '@ "02e9e0002e-U0S1I4" "Identify Device" "IdentifyDevice" "IdentifyDevice" "deviceId":"D2U0S1I4" "deviceType":"interface" "rootId":"02e9e0002e" "interfaceType":"output" "unitId":"U1" '
./sendUdpPacket.py '@ "02e9e0002e-U0S1I342458095" "Identify Input Device" "IdentifyInputDevice" "IdentifyInputDevice" "deviceId":"D2U0S1I342458095" "deviceType":"interface" "rootId":"02e9e0002e" "interfaceType":"output" "unitId":"U1" '
./sendUdpPacket.py '@ "02e9e0002e-U0S1I257" "TamperDetector" "TamperDetector" "TamperDetector" "deviceId":"D2U0S1I257" "deviceType":"interface" "rootId":"02e9e0002e" "interfaceType":"output" "unitId":"U1" '
./sendUdpPacket.py '@ "02e9e0002e-U0S1I272" "BatteryIndicator" "BatteryIndicator" "BatteryIndicator" "deviceId":"D2U0S1I272" "deviceType":"interface" "rootId":"02e9e0002e" "interfaceType":"output" "unitId":"U1" '
./sendUdpPacket.py '@ "02e9e0002e-U0S1I277" "Active Device" "ActiveDevice" "ActiveDevice" "deviceId":"D2U0S1I277" "deviceType":"interface" "rootId":"02e9e0002e" "interfaceType":"output" "unitId":"U1" '
./sendUdpPacket.py '@ "02e9e0002e-device" "Window Open Detector" "dectWindowOpenCloseDetector" "dectWindowOpenCloseDetector" "deviceId":"02e9e0002e" "deviceType":"root"'
./sendUdpPacket.py '@ "02e9e0002e-U1S1I256" "Alert" "Alert" "Alert" "deviceId":"D2U1S1I256" "deviceType":"interface" "rootId":"02e9e0002e" "interfaceType":"output" "unitId":"U1" '
./sendUdpPacket.py '@ "02e9e0002e-device" "Window Open Detector" "dectWindowOpenCloseDetector" "dectWindowOpenCloseDetector" "deviceId":"02e9e0002e" "deviceType":"root" "Response Time":"0" "Software Version":"151934" "Hardware Version":"dhx91-ooma-c" "Manufacturer":"Ooma"' 


Remove sensor interface
./sendUdpPacket.py 'R "02e9e0002e-device" "Window Open Detector" "dectWindowOpenCloseDetector" "dectWindowOpenCloseDetector" "deviceId":"02e9e0002e" "deviceType":"root" "Response Time":"0" "Software Version":"151934" "Hardware Version":"dhx91-ooma-c" "Manufacturer":"Ooma"' 


Send alert
./sendUdpPacket.py 'c D2U1S1I256 0'

'''
