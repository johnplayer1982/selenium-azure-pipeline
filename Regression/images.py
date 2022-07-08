from selenium.webdriver.common.by import By
from importlib.machinery import SourceFileLoader
import time

def runTest(baseUrl, driver):

    urls = [
        "/en",
        "/cy"
    ]

    for url in urls:

        # 3600 - Home page: image under ‘Why choose us?’ is loading 3×
        print('\n 3600 - {} Home page: image under ‘Why choose us?’ is loading 3×'.format(url))
        iterationUrl = "{baseUrl}{url}".format(baseUrl=baseUrl, url=url)
        driver.get(iterationUrl)

        # Store the 3 why choose us images
        whyChooseImages = driver.find_elements(By.CSS_SELECTOR, '.cmp-image__image')
        assert len(whyChooseImages) == 1
        print('- Only 1 image in "Why choose us" loaded')
