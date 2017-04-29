from bb_send_command import send_command

class bb_gpio_process():
    def __init__(self):
        self.cmd = ""
        self.gpio_dict = {
                            "pair" : 0,
                            "tamper" : 1,
                            "event" : 2
                        }

        self.switch = {
                            "on" : 1,
                            "off" : 0
                       }


    def process_door_sensor_request(self, interface, switch_state):
        # self.cmd = "c d2i" + str(self.gptfio_dict[interface]) + " " + str(self.switch[switch_state])
        self.cmd = "c d3i" + str(self.gpio_dict[interface]) + " " + str(self.switch[switch_state])

        response = "Going to Process the Door Sensor"
        send_command(self.cmd)
        return response

    def process_water_sensor_request(self, interface, switch_state):
        self.cmd = "c d2i" + str(self.gpio_dict[interface]) + " " + str(self.switch[switch_state])
        response = "Going to Process the Water Sensor"
        send_command(self.cmd)
        return response

    def process_motion_sensor_request(self, interface, switch_state):
        self.cmd = "c d1i" + str(self.gpio_dict[interface]) + " " + str(self.switch[switch_state])
        response = "Going to Process the Motion Sensor"
        send_command(self.cmd)
        return response



