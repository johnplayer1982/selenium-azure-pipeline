import time
from selenium.webdriver.common.by import By

def dismissCookieBanner(driver):
    time.sleep(1)
    
    try:
        cookieElemBtn = driver.find_element(By.CSS_SELECTOR, "#ccc-notify-accept")
        cookieElemBtn.click()
        print(' - Cookie banner dismissed')
    except:
        print(' - Cookie banner not found, either previously dismissed or testing on test environment')
        pass
