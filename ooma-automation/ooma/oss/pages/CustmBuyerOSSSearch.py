from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait as WT
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datetime, time



class CustmBuyerOSSSearch():
    def __init__(self, driver):
        self.driver = driver

    def myxid_look(self, myxid):
        driver = self.driver
        myxid = "227D8E"
        # Now we need to wait for the new page to display so we are going to do
        #   1. Create a webdriver wait with a timeout of 300 seconds
        #   2. we are waiting until some element from new page is being displayed
        waittime = WT(driver, 300)
        # now here we are waiting until we see buyerform in the new page
        waittime.until(EC.presence_of_element_located((By.ID, 'buyerForm')))

        # Now we are going to enter the Hub ID or myxid
        # getting the forms to see the current form
        forms_list = driver.find_elements_by_xpath("//form//input")
        for form_ele in forms_list:
            # print "current form is : ::: ",form_ele.get_attribute("id")
            myxid_ele = form_ele.get_attribute("id")
            #print "current element id is : ", myxid_ele
            if myxid_ele.startswith("buyer"):
                form_ele.click()
                form_ele.send_keys(myxid)
                form_ele.send_keys(Keys.RETURN)
                break


    def newdef(self):
        pass