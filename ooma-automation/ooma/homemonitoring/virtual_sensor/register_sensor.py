from homemonitoring.setup.json_parse import JsonConfig
import os, json

class Register_sensor():
    def __init__(self):
        self.json_obj = JsonConfig()

    def get_the_sensor_details(self):
