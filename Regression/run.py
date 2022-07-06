from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os, requests, breadcrumbs

username = os.getenv("CBT_USERNAME")
authkey = os.getenv("CBT_AUTHKEY")

api_session = requests.Session()
api_session.auth = (username, authkey)
test_result = None

caps = {
 'platform': 'Windows',
 'browserName': 'Chrome',
}

driver = webdriver.Remote(
    command_executor="http://%s:%s@hub.crossbrowsertesting.com/wd/hub"%(username, authkey),
    desired_capabilities=caps)

baseUrl = "https://test.moneyhelper.org.uk"
tests = {
    "Breadcrumbs" : breadcrumbs,
}

try:
    for key, value in tests.items():
        value.runTest(baseUrl, driver)
    test_result = 'pass'
except AssertionError as e:
    test_result = 'fail'
    raise

print("Done with session %s" % driver.session_id)
driver.quit()
# Here we make the api call to set the test's score.
# Pass it it passes, fail if an assertion fails, unset if the test didn't finish
if test_result is not None:
    api_session.put('https://crossbrowsertesting.com/api/v3/selenium/' + driver.session_id,
        data={'action':'set_score', 'score':test_result})
