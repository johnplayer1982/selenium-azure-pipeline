from selenium.webdriver.common.by import By
from importlib.machinery import SourceFileLoader
import time

def getImageSize(selector):
    image = selector
    width = image.size["width"]
    height = image.size["height"]
    return [width, height]

def runTest(baseUrl, driver):

    resize = SourceFileLoader('getresize', '../Lib/resize.py').load_module()
    teaser_warnings = set()

    locales = {
        "/en",
        "/cy"
    }

    for locale in locales:

        # Define the URL to visit based on the locale
        iterationUrl = "{url}{locale}/blog".format(url=baseUrl, locale=locale)
        driver.get(iterationUrl)
        resize.resizeDesktop(driver)
        time.sleep(1)
        print("\nVisiting {url}{locale}/blog".format(url=baseUrl, locale=locale))

        # For some reason the markup on the Welsh version is different from the English
        if locale == "/en":
            threeColumnTeaserSelector = ".cmp-blog-posts__item--three-column"
        else:
            threeColumnTeaserSelector = ".aem-GridColumn--default--4"
        threeColumnTeasers = driver.find_elements_by_css_selector(threeColumnTeaserSelector)

        # Print out how many of each teaser was found on the page
        print("\n -----")
        print("| {num} three column teasers found on page".format(num=len(threeColumnTeasers)))
        print(" -----\n")

        print("\n")

        # 3 column teasers
        threeColLen = len(threeColumnTeasers)
        if threeColLen > 0:
            print("+ Testing {threeColLen} three column teasers".format(threeColLen=threeColLen))

            # All images sizes should be the same
            driver.maximize_window()
            print("- Maximising window")

            expectedHeight = 199
            expectedWidth = 398
            threeColCount = 0

            for teaser in threeColumnTeasers:
                
                if locale == "/en":
                    teaserImage = teaser.find_element(By.CSS_SELECTOR, ".cmp-blog-posts__item--three-column-image")
                else:
                    teaserImage = teaser.find_element(By.CSS_SELECTOR, ".cmp-teaser__link-image")

                threeColCount += 1

                teaserImageDimensions = getImageSize(teaserImage)

                teaserImageWidth = teaserImageDimensions[0]
                teaserImageHeight = teaserImageDimensions[1]

                if teaserImageHeight == expectedHeight and teaserImageWidth == expectedWidth:
                    print("- Teaser image {threeColCount} is as expected {teaserImageWidth}px x {teaserImageHeight}px".format(threeColCount=threeColCount, teaserImageWidth=teaserImageWidth, teaserImageHeight=teaserImageHeight))
                else:
                    print('> WARNING: Teaser dimensions incorrect on {}'.format(iterationUrl))

        else:
            print("- No 2 column teasers found")
    
    # Confirm that the teaser heights are consistent for varying content
    toolsUrl = "{}/en/tools-and-calculators".format(baseUrl)
    driver.get(toolsUrl)
    driver.maximize_window()
    # Get the grids
    grids = driver.find_elements(By.CSS_SELECTOR, '.grid')
    for grid in grids:
        # Get the teasers
        teasers = grid.find_elements(By.CSS_SELECTOR, '.cmp-teaser__wrapper')

        if len(teasers) > 0:
            baseHeight = teasers[0].value_of_css_property('height')
            for teaser in teasers:
                teaserHeight = teaser.value_of_css_property('height')
                # confirm the height of the teasers are consistent
                if teaserHeight != baseHeight:
                    teaser_warnings.add('> WARNING: Teasers are inconsistent height on {}'.format(toolsUrl))

    for warning in teaser_warnings:
        print(warning)
