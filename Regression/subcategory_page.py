from selenium.webdriver.common.by import By
from importlib.machinery import SourceFileLoader

def runTest(baseUrl, driver):

    subcategorypages = SourceFileLoader('getsubcategorypages', '../Lib/subcategory_pages.py').load_module()
    urls = subcategorypages.get_subcategory_pages()

    for page in urls:

        landingPageUrl = "{baseUrl}{page}".format(baseUrl=baseUrl, page=page)
        driver.get(landingPageUrl)
        print("\nVisiting {landingPageUrl}".format(landingPageUrl=landingPageUrl))

        # Check the page has a H1 and it contains content
        heading = driver.find_element(By.CSS_SELECTOR, "h1.cmp-title__text").text
        headingLen = len(heading)
        assert headingLen > 0
        print("- Page heading found: {heading} ({headingLen} characters)".format(heading=heading, headingLen=headingLen))
        
        # Check dimensions of the feature image
        featureImage = driver.find_element(By.CSS_SELECTOR, ".cmp-image")
        assert featureImage
        print('- Feature image found')
        featureImageSize = featureImage.size
        height = featureImageSize["height"]
        width = featureImageSize["width"]
        assert height > 30 or width > 100

        # Check if there are article links on the page
        articleLinks = driver.find_elements(By.CSS_SELECTOR, ".cmp-list-of-articles__links-list-item")
        articleLinksCount = len(articleLinks)
        assert articleLinksCount >= 1
        print("- {articleLinksCount} article links found".format(articleLinksCount=articleLinksCount))
