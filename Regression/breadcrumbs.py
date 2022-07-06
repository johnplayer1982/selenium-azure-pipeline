
def runTest(baseUrl, driver):
    testArticle = "{baseUrl}/content/maps/money-helper/en/jp-test/how-to-choose-the-right-bank-account.html?wcmmode=disabled".format(baseUrl=baseUrl)
    driver.get(testArticle)