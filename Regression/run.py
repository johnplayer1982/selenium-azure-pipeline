from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os, breadcrumbs

username = os.getenv("CBT_USERNAME")
authkey = os.getenv("CBT_AUTHKEY")


caps = {
 'platform': 'Windows',
 'browserName': 'Chrome',
}

driver = webdriver.Remote(
    command_executor="http://%s:%s@hub.crossbrowsertesting.com/wd/hub"%(username, authkey),
    desired_capabilities=caps)

baseUrl = "https://test.moneyhelper.org.uk"

breadcrumbs.runTest()
driver.quit()
