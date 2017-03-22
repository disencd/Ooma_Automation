from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait as WT
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import datetime, time

class CustomerDetailsPage():
    def __init__(self, driver):
        self.driver = driver
        self.accces_href_elements()
    #Returns a list that have href element like  Transactions
    # -> Myx Notify -> Deposit VM
    #-> LEC Info 	-> Change SPN
    # -> Services 	-> E911
    # -> Orders & Products 	-> Users
    # -> Credit Cards ->  	-> CP Events+
    # -> Accounting 	->Prepaid Acct
    # -> Cancel Customer 	-> Debug Telo
    # -> LNP Workflow  	-> Cust Config

    def accces_href_elements(self):
        driver = self.driver

        #Added the digits for sorting the dictionary properly
        self.acc_mgt_dict = {"01_Data_Center" : [],
                        "02_Myx_Notify" : [],
                        "03_Orders_n_Products" : [],
                        "04_Users" : [],
                        "05_Credit_Cards" : [],
                        "06_Add_Credit_Cards" : [],
                        "07_CP_Events" : [],
                        "08_Add_CP_Events" : [],
                        "09_Accounting" : [],
                        "10_Prepaid_Acct" : [],
                        "11_Cancel_Customer" : [],
                        "12_LNP Workflow" : [],
                        "13_Deposit_VM" : []
                        }

        # Now we need to wait for the new page to display so we are going to do
        #   1. Create a webdriver wait with a timeout of 300 seconds
        #   2. we are waiting until some element from new page is being displayed
        waittime = WT(driver, 3)
        time.sleep(3)
        # now here we are waiting until we see invisibleLink in the new page
        waittime.until(EC.presence_of_element_located((By.ID, 'customer_details_header')))

        # Now login Cick the invisiblelink - accessed using the xpath
        dev_srch_lst = driver.find_elements_by_xpath("//a")

        # Instead of searching the whole page, we want to get all the a tags in a specific area.
        #dev_srch_lst = driver.find_elements_by_xpath("//div[@style='margin-left']//a")
        #print dev_srch_lst
        for form_ele in dev_srch_lst:
            # Searching based on the class as invisibleLink
            # dev_ele = form_ele.get_attribute("href")

            title_elem = form_ele.get_attribute("title")
            if title_elem:
                element_list = []
                element_list.append(title_elem)
                element_list.append(form_ele.get_attribute("href"))
                #print element_list
                first_flag = 0
                #Sorting the dictionary b/s dictionary is printed uneven
                for key in sorted(self.acc_mgt_dict):
                    if not self.acc_mgt_dict[key] and not first_flag:
                        #Creating dict with the correct names
                        self.acc_mgt_dict[key] = element_list
                        #One element has to be filled only once
                        first_flag = 1
                        break
        print "********************************************"
        #print self.acc_mgt_dict
        print "********************************************"

    def cancel_click(self):
        driver = self.driver
        #cancel_elem = self.acc_mgt_dict["11_Cancel_Customer"][1]

        customer_handle = driver.current_window_handle

        #print "current customer window handle is : ", customer_handle


        driver.find_element_by_partial_link_text('Cancel').click()
        waittime = WT(driver, 3)
        #time.sleep(3)
        # now here we are waiting until we see invisibleLink in the new page
        waittime.until(EC.visibility_of_any_elements_located((By.ID,"cancelDiv")))
        # waittime.until_not(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//div[@id='cancelDiv']")))

        # Getting all the iframes

        iframe_eles = driver.find_elements(By.TAG_NAME, "iframe")
        for iframe_ele in iframe_eles:
            #print iframe_ele
            iframe_title= iframe_ele.get_attribute('id')
            if iframe_title == "cancelFrame":
                driver.switch_to_frame(iframe_title)
                # doc_elements = driver.find_elements(By.XPATH,"#document/html/head/title")
                doc_elements = driver.find_element_by_xpath("//th[@class='popUpHeader']")
                print "Dropdown elements " , doc_elements.text
                select_options_list = driver.find_elements(By.XPATH, "//select[@id='reasonPk']//option")
                #selectobj = Select(driver.find_element_by_id("reasonPk"))
                #print "After selecting object" , selectobj
                #selectobj.select_by_index(3)
                for option_name in select_options_list:
                    print option_name.text
                    if option_name.text == "Returned Device":
                        #selectobj.select_by_value(option_name.text)

                        #Select.select_by_index(5)
                        break

                text_list = driver.find_element_by_id("comment")
                text_list.send_keys("Python Selenium Automation is returning the Device")
