from selenium.webdriver.common.by import By
from importlib.machinery import SourceFileLoader
import time

def runTest(baseUrl, driver):

    print("\nSTART OF MISC TESTS")
    print("===================")

    # 3444 - MH to MH Redirects pointing to http instead of https - extra hop happening. Investigation required.
    print('- Testing MH to MH Redirects pointing to http instead of https, Ticket 3444')
    targetUrl = "https://www.moneyhelper.org.uk/blog/how-stock-market-falls-affect-your-retirement-income"
    driver.get(targetUrl)
    expectedURL = "https://www.moneyhelper.org.uk/en/pensions-and-retirement/taking-your-pension/what-is-flexible-retirement-income-pension-drawdown"
    assert driver.current_url == expectedURL
    print(' + Example redirect pointing to https')

    print('- Welsh language URL: helpwrarian.org.uk to moneyhelper.org.uk/cy, Ticket 2827')
    targetUrl = "https://www.moneyhelper.org.uk/cy"
    driver.get("http://www.helpwrarian.org.uk")
    time.sleep(2)
    currentUrl = driver.current_url
    assert currentUrl == targetUrl
    print(' + Welsh language URL: helpwrarian.org.uk displaying welsh homepage OK')
    
    # 3590 - Favicons incorrect on Safari, Ticket 3590
    print('\n3590 - Favicons incorrect on Safari')
    driver.get(baseUrl)
    faviconTag = driver.find_element(By.CSS_SELECTOR, 'link[rel="mask-icon"]')
    faviconTagColor = faviconTag.get_attribute('color')
    expectedColour = "#C82A87"
    assert faviconTagColor == expectedColour
    print(' - Favicon colour correct on Safari')
