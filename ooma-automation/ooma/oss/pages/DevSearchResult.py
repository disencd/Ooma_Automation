
from selenium import webdriver

#from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait as WT
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datetime, time

class DeviceSearchResult():
    def __init__(self, driver):
        self.driver = driver

    def access_registrant(self):
        driver = self.driver
        # Now we need to wait for the new page to display so we are going to do
        #   1. Create a webdriver wait with a timeout of 300 seconds
        #   2. we are waiting until some element from new page is being displayed
        waittime = WT(driver, 3)
        time.sleep(3)
        # now here we are waiting until we see invisibleLink in the new page
        waittime.until(EC.presence_of_element_located((By.ID, 'homePageLink')))

        #Now login Cick the invisiblelink - accessed using the xpath
        dev_srch_lst = driver.find_elements_by_xpath("//a")
        for form_ele in dev_srch_lst:
            #Searching based on the class as invisibleLink
            dev_ele = form_ele.get_attribute("class")

            if dev_ele.startswith("invisibleLink"):
                form_ele.click()