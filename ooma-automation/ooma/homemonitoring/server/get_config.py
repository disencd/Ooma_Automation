from homemonitoring.server.hms import HMS
from homemonitoring.server.server_cb import cb_client

class GetSensorConfig(object):

    def get_sensor_status(self):
        cb_obj = cb_client(sensor_status)

    def get_sensor_tamper_status(self):
        pass

    def get_sensor_pair_status(self):
        pass

    def get_sensor_paging_status(self):
        pass

    def get_sensor_event_status(self):
        pass

class GetModeConfig(object):

    def __init__(self):
        pass

    def get_mode_settings(self):
        pass

class GetNotificationConfig(object):

    def __init__(self):
        pass

    def get_notification_settings(self):
        pass

    def get_email_notification_settings(self):
        pass

    def get_sms_notification_settings(self):
        pass

    def get_phone_notification_settings(self):
        pass

