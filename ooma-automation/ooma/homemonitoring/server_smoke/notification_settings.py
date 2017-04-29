import json

from homemonitoring.server.hms import HMS

DEVICE_ID = None

class NotificationSettings(object):
    url = "api/devices/%s/notification_settings"
    modes = {}
    def _get_mode_name(self):
        return self.__class__.__name__.split("Mode")[0]

    def __init__(self):

        data, code = HMS().request("api/modes").get()
        assert (code == 200), "Cannot get modes"
        data = json.loads(data)
        self.modes = { d['name']: d['id'] for d in data}

    def __get__(self, obj, objtype):

        id = self.modes[self._get_mode_name()]\
            if self._get_mode_name() != "All" else ""
        assert id is not None, "Mode was not found"
        assert DEVICE_ID, "Device id was not set"
        response = HMS().request("%s/%s"%(self.url % DEVICE_ID, id)).get()
        print "RESPONSE: ", response
        #print response
        return response

    def __set__(self, obj, val):
        id = self.modes[self._get_mode_name()]\
            if self._get_mode_name() != "All" else ""
        assert id is not None, "Mode was not found"
        assert isinstance(val, dict), "Should be a dict"
        response = HMS().request("%s/%s"%(self.url % DEVICE_ID, id)).post(val)
        #print response
        return response  

class AllModes(NotificationSettings): pass
class HomeMode(NotificationSettings): pass
class AwayMode(NotificationSettings): pass
class NightMode(NotificationSettings): pass
    
class NotificationSettingsHandler(object):
    home_mode = HomeMode()
    away_mode = AwayMode()
    night_mode = NightMode()
    all_modes = AllModes()

class CustomMode(object):
    url = "api/modes"
    id = None
    #mode = NotificationSettings()

    def create(self, name):
        assert self.id is None, "Mode already created."
        data, code = HMS().request(self.url).post({"name": name})
        assert (code == 200), "Cannot create custom mode"            
        data = json.loads(data)
        self.id = data["id"]
        return data

    def get(self):
        data, code = HMS().\
                     request("{0}/{1}".format(self.url, self.id)).\
                     get()
        assert (code == 200), "Cannot create custom mode"  
        data = json.loads(data)
        return data
        

    def update(self, val):
        assert isinstance(val, dict), "Should be a dict"       
        data, code = HMS().request("%s/%s"%(self.url, self.id)).post(val)
        assert (code == 200), "Cannot update custom mode"  
        data = json.loads(data)
        return data

    def delete(self):
        if self.id:
            data, code = HMS().\
                         request("{0}/{1}".format(self.url, self.id)).\
                         delete()
            assert (code == 200), "Cannot create custom mode"
            self.id = None
        else:
            print "Nothing to delete"


class CurrentMode(object):
    url = "api/modes/current"
    id = None
    modes = {}
    allow = ["Away", "Home", "Night"]

    def __init__(self):
        data, code = HMS().request("api/modes").get()
        assert (code == 200), "Cannot get modes"
        data = json.loads(data)
        self.modes = {d['name']: d['id'] for d in data}

    def get(self):
        data, code = HMS().request(self.url).get()
        assert (code == 200), "Cannot create custom mode"
        data = json.loads(data)
        return {data['name']: data['id']}

    def set(self, mode):
        assert mode in self.allow, "Should be ".__add__(", ".join(self.allow))
        mode = {"id" : self.modes[mode],
                "name": mode}

        data, code = HMS().request(self.url).post(mode)
        assert (code == 200), "Cannot update custom mode"
        data = json.loads(data)
        return data



#mode = CurrentMode()
#c = mode.get()
#print c
#l = mode.set('Away')
#print l
#c = mode.get()
#print c


#mode = CustomMode()
#mode.create("Mode4")
#mode.get()
#mode.update('Mode2')
#mode.delete()

#c = NotificationSettingsHandler()
#print c.night_mode
#print c.all_modes
#c.all_modes = new_notification_settings
#c.night_mode = new_notification_settings

