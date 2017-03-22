from selenium.webdriver.common.keys import Keys

class Account_Activation():
    def __init__(self, driver, json_conf):
        self.driver = driver
        self.act_code = json_conf["device_credentials"]["activ_code"]

    def enter_actcode(self):
        # Find element by ID - "mac_address"
        mac_elem = self.driver.find_element_by_id("mac_address")
        print "enter_actcode method-- ", mac_elem
        mac_elem.send_keys(self.act_code)
        print "adding the myxid ", self.act_code
        mac_elem.send_keys(Keys.RETURN)
