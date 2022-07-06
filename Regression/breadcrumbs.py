from selenium.webdriver.common.by import By
from importlib.machinery import SourceFileLoader

def runTest(baseUrl, driver):

    dismisscookie = SourceFileLoader('getcookiefile', '../Lib/dismisscookie.py').load_module()
    articlelist = SourceFileLoader('getarticlelist', '../Lib/article_list.py').load_module()
    resize = SourceFileLoader('getresize', '../Lib/resize.py').load_module()

    testArticle = "{baseUrl}/en/jp-test/how-to-choose-the-right-bank-account".format(baseUrl=baseUrl)
    driver.get(testArticle)
    dismisscookie.dismissCookieBanner(driver)
    articlelist = articlelist.get_articles()
    for article in articlelist:
        iterationUrl = "{baseUrl}{article}".format(baseUrl=baseUrl, article=article)
        driver.get(iterationUrl)
        print('\n Visiting {}'.format(iterationUrl))
        expectedHeight = 61
        
        # Desktop
        resize.resizeDesktop(driver)

        # Finding Breadcrumbs
        desktopBreadcrumbs = driver.find_element(By.CSS_SELECTOR, '.breadcrumb')
        desktopBreadcrumbsList = desktopBreadcrumbs.find_element(By.CSS_SELECTOR, '.cmp-breadcrumb__list')
        desktopBreadcrumbItems = desktopBreadcrumbsList.find_elements(By.CSS_SELECTOR, '.cmp-breadcrumb__list-item')
        itemCount = len(desktopBreadcrumbItems)
        expectedLength = 3

        # Confirm the correct amount of levels are found on the article (Home > L1 > L2)
        assert itemCount == expectedLength
        print('- {itemCount} breadcrumb links found, 3 expected'.format(itemCount=itemCount))
        
        # Confirm the 1st link is to the homepage
        if "en/" in iterationUrl:
            homeLinkText = "Home"
        else:
            homeLinkText = "Hafan"
        assert desktopBreadcrumbItems[0].text == homeLinkText
        print('- 1st link in breadcrumb correct "{homeLinkText}"'.format(homeLinkText=homeLinkText))
        
        # Confirm height of desktop breadcrumb
        actualHeight = desktopBreadcrumbs.size['height']
        
        assert actualHeight == expectedHeight
        print('- Desktop breadcrumb correct height {actualHeight}px'.format(actualHeight=actualHeight))

        # Switch to mobile
        resize.resizeMobile(driver)
        print('- Switching to mobile')
        expectedHeight = 58 # 55px breadcrumb + 3px border
        mobileBreadcrumb = driver.find_element(By.CSS_SELECTOR, '.cmp-breadcrumb__list--mobile')

        # Mobile height
        actualHeight = mobileBreadcrumb.size['height']

        assert actualHeight == expectedHeight
        print('- Breadcrumb is expected height for mobile')
        
        breadcrumb = driver.find_element(By.CSS_SELECTOR, 'a.cmp-breadcrumb__list--mobile')
        breadcrumbHref = breadcrumb.get_attribute("href")
        assert not ".html" in breadcrumbHref or "/content/maps/moneyhelper/" in breadcrumbHref
        print(' - Breadcrumb href does not contain .html or /content/maps/moneyhelper/ path (5082)')
