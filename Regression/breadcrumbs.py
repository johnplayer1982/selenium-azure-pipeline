from importlib.machinery import SourceFileLoader

dismisscookie = SourceFileLoader('getcookiefile', '../Lib/dismisscookie.py').load_module()

def runTest(baseUrl, driver):
    testArticle = "{baseUrl}/en/jp-test/how-to-choose-the-right-bank-account".format(baseUrl=baseUrl)
    driver.get(testArticle)
    dismisscookie.dismissCookieBanner(driver)
    print('- Cookie banner dismissed')
