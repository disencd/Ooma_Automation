from selenium.webdriver.common.keys import Keys

class Oss_login():
    def __init__(self, driver):
        self.driver = driver

    def oss_login(self, usr, pwd):
        driver = self.driver

        # Find element by ID - "username"
        user_elem = driver.find_element_by_id("username")

        # Edit the username in box
        user_elem.send_keys(usr)

        # Find element by ID - "dummypassword"
        pwd_elem = driver.find_element_by_id("dummypassword")

        # Edit the password in box
        bool = pwd_elem.get_attribute('readonly')

        if bool:
            # Remove onfocus - readonly attribute
            driver.execute_script('arguments[0].removeAttribute("readonly", "readonly")', pwd_elem)

            # Edit the password
            pwd_elem.send_keys(pwd)
        print "Logged in to OSS Console"
        # We are now pressing the return/enter button to login.
        pwd_elem.send_keys(Keys.RETURN)
