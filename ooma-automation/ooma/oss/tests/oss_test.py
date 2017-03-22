import unittest

from selenium import webdriver

from oss.pages.CustmBuyerOSSSearch import CustmBuyerOSSSearch
from oss.pages.DevSearchResult import DeviceSearchResult
from oss.pages.WebAccountActivation import Account_Activation
from oss.pages.customers.CustDetails1 import CustomerDetailsPage
from oss.pages.ossloginpage import Oss_login
from oss.setup.config_oss import JsonConfig


#Unittest framework for testing the OSS Functionalities
class OSStest(unittest.TestCase):

    def setUp(self):
        print "Setting up OSS Test Automation"
        #Loading the Json configuration details
        jsonobj = JsonConfig()
        self.jconfig = jsonobj.dump_config()


    def test_Cancel(self):
        print "OSS Cancel Testcase Executing"
        self.oss_driver = webdriver.Firefox()
        self.oss_driver.get(self.jconfig["sandbox"]["oss_url"])

        oss_obj = Oss_login(self.oss_driver)

        #Fetching the OSS Access credentials & Myxid
        username = self.jconfig["oss_login"]["username"]
        password = self.jconfig["oss_login"]["password"]
        myxid = self.jconfig["device_credentials"]["myxid"]
        oss_obj.oss_login(username, password)

        myxid_obj = CustmBuyerOSSSearch(self.oss_driver)
        myxid_obj.myxid_look(myxid)
        dev_obj = DeviceSearchResult(self.oss_driver)
        dev_obj.access_registrant()
        cust_obj = CustomerDetailsPage(self.oss_driver)
        cust_obj.cancel_click()
        self.oss_driver.close()

    def test_activation(self):
        print "Account Activation Code"
        self.act_driver = webdriver.Firefox()
        self.act_driver.get(self.jconfig["sandbox"]["activation_url"])

        self.act_obj = Account_Activation(self.act_driver, self.jconfig)

    def tearDown(self):
        pass
        #self.oss_driver.quit()


if __name__ == "__main__":
    unittest.main()