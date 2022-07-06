from importlib.machinery import SourceFileLoader

def runTest(baseUrl, driver):

    dismisscookie = SourceFileLoader('getcookiefile', '../Lib/dismisscookie.py').load_module()
    articlelist = SourceFileLoader('getarticlelist', '../Lib/article_list.py').load_module()

    testArticle = "{baseUrl}/en/jp-test/how-to-choose-the-right-bank-account".format(baseUrl=baseUrl)
    driver.get(testArticle)
    dismisscookie.dismissCookieBanner(driver)
    articlelist = articlelist.get_articles()
    for article in articlelist:
        iteration_url = "{baseUrl}{article}".format(baseUrl=baseUrl, article=article)
        driver.get(iteration_url)
        print('\n Visiting {}'.format(iteration_url))
