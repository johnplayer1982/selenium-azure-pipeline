from selenium.webdriver.common.by import By
from importlib.machinery import SourceFileLoader
import time

def runTest(baseUrl, driver):

    resize = SourceFileLoader('getresize', '../Lib/resize.py').load_module()
    articlelist = SourceFileLoader('getarticlelist', '../Lib/article_list.py').load_module()

    locale = {
        "/en": "Got a pension question?",
        "/cy": "Oes gennych chi bensiwn?"
    }

    for key, value in locale.items():

        print("\nSTART OF {key} EMERGENCY BANNER TESTS".format(key=key))
        print("======================================")

        # Start test in desktop view
        resize.resizeDesktop(driver)

        # Visit the correct baseUrl for each language
        iterationbaseUrl = "{baseUrl}{key}".format(baseUrl=baseUrl, key=key)
        driver.get(iterationbaseUrl)
        print("Visiting {iterationbaseUrl}".format(iterationbaseUrl=iterationbaseUrl))
        time.sleep(2)

        # Check the emergency banner is present
        emergencyBanner = driver.find_element_by_css_selector(".emergency-banner")
        # If it is visible then run our tests
        if emergencyBanner.size['height'] > 0:
            print("- Emergency banner found")

            # Check the language (using the 1st bolded text)
            emergencyBannerText = driver.find_element_by_css_selector(".cmp-emergency-banner__message-description strong").text
            assert value in emergencyBannerText
            print("- Banner text is correct language: {text}".format(text=emergencyBannerText))
            
            # Close the banner - outside of the loop as dismissing english also dismisses welsh and vice versa
            emergencyBannerClose = driver.find_element_by_css_selector(".cmp-emergency-banner__close.cmp-emergency-banner__actions-button")
            assert emergencyBannerClose
            emergencyBannerClose.click()
            print("- Clicking the close button")
            
            time.sleep(1)

            # Confirm banner not visible
            assert driver.find_element_by_css_selector(".cmp-emergency-banner").get_attribute("style") == "display: none;"
            print("- Emergency banner is hidden")

            # Confirm cookie is set
            all_cookies = driver.get_cookies()
            cookieStr = str(all_cookies)
            assert "emergency_banner" in cookieStr
            print("- 'emergency_banner' Cookie set in necessary cookies")
            
            # Navigate to a number of pages to confirm the banner is not visible, cookie set and being acted on
            articleUrls = articlelist.get_articles()
            print('- Checking a few pages')

        for url in articleUrls:

            url = url[0]
            iterationUrl = "{baseUrl}{url}".format(baseUrl=baseUrl, url=url)
            driver.get(iterationUrl)

            # If the banner size is not greater than 1px tall, in other words visible
            assert not driver.find_element(By.CSS_SELECTOR, ".emergency-banner").size['height'] >= 1
            print(' + Emergency banner hidden on {iterationUrl}'.format(iterationUrl=iterationUrl))
