from selenium import webdriver
import os
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import subprocess
from selenium.webdriver.chrome.options import Options
import logging

class BrowserSetup(object):


    def logout(self):
        self.switchToTab("account")
        self.driver.find_element_by_id("logout_button").click()

    
    def setupDriver(self):
        self.driver = self.getDriver()
        self.driver.implicitly_wait(5)
        self.driver.set_page_load_timeout(20)
        return self.driver

    def _switchWindow(self,driver):
        self.master = driver.current_window_handle
        timeCount = 1;
        while (len(driver.window_handles) == 1 ):
            timeCount += 1
            if ( timeCount > 50 ): 
                break;
        for handle in driver.window_handles:
            if handle!=self.master:
                driver.switch_to.window(handle)


    def deleteCerts(self):
        if os.environ.get("WEBDRIVER", None) == "chrome":
            delete_script = os.path.join(os.path.dirname(__file__), "..", "..", "..", "tools", "delcerts")
            retcode = subprocess.call(delete_script)
            self.assertEqual(retcode, 0)

