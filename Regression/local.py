from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os, requests
import cookies, breadcrumbs, accordion_carousel, article_feedback, blog_post, callouts, chat, emergency_banner
from selenium.webdriver.chrome.options import Options

baseUrl = "https://test.moneyhelper.org.uk"

# driver = webdriver.Safari()
CHROME_VERSION_PC = os.getenv('CHROME_VERSION_PC')
DRIVER_BIN = "..\chromedriver_104.exe"
options = Options()
options.binary_location = r"C:\Program Files\Google\Chrome Beta\Application\chrome.exe"
driver = webdriver.Chrome(chrome_options=options, executable_path=DRIVER_BIN)

tests = {
    # "Cookies" : cookies,
    # "Breadcrumbs" : breadcrumbs,
    # "Accordion Carousel" : accordion_carousel,
    # "Article Feedback" : article_feedback,
    # "Blog Post" : blog_post,
    # "Callouts" : callouts,
    # "Chat" : chat,
    "Emergency Banner" : emergency_banner,
}

for key, value in tests.items():
    print('> Testing {}\n'.format(key))
    value.runTest(baseUrl, driver)
    print('\n> End of {} test\n'.format(key))

driver.quit()
