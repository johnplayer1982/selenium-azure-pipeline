from selenium.webdriver.common.by import By
from importlib.machinery import SourceFileLoader

def runTest(baseUrl, driver, browser):

    print(' - Testing on {}'.format(browser))
    resize = SourceFileLoader('getresize', '../Lib/resize.py').load_module()
    articlelist = SourceFileLoader('getarticlelist', '../Lib/article_list.py').load_module()

    urls = articlelist.get_articles()

    for url in urls:

        # Construct the full URL
        iterationUrl = "{baseUrl}{url}".format(baseUrl=baseUrl, url=url)
        # Visit the URL
        driver.get(iterationUrl)
        print("\nVisiting {iterationUrl}".format(iterationUrl=iterationUrl))

        # Start with the max screen size
        driver.maximize_window()
        print("- Maximising window")

        contentContainers = driver.find_elements(By.CSS_SELECTOR, '.aem-Grid')
        # Get all text components on the page
        textComponents = contentContainers[15].find_elements(By.CSS_SELECTOR, 'div.cmp-text')
        # Iterate through the text components
        for text in textComponents:
            # Get all of the tags
            allTags = text.find_elements(By.CSS_SELECTOR, '*')
            # Make sure the last element does not have a bottom margin (Release 1.7.6 Ticket 3603)
            pTagsLen = len(allTags)
            lastTag = allTags[pTagsLen - 1]
            lastPMargin = lastTag.value_of_css_property('margin-bottom')
            # If the last element has no bottom margin then we are good
            assert lastPMargin == "0px"
        print('- Last element in text components have no bottom margin as expected')
