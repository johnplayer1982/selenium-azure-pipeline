from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os, requests, breadcrumbs, accordion_carousel

baseUrl = "https://test.moneyhelper.org.uk"

driver = webdriver.Safari()

tests = {
    "Breadcrumbs" : breadcrumbs,
    "Accordion Carousel" : accordion_carousel,
}

for key, value in tests.items():
    print('> Testing {}\n'.format(key))
    value.runTest(baseUrl, driver)
    print('\n> End of {} test\n'.format(key))
