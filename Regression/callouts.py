from xml import dom
from selenium.webdriver.common.by import By
from importlib.machinery import SourceFileLoader

def runTest(baseUrl, driver, browser):
    
    print(' - Testing on {}'.format(browser))
    resize = SourceFileLoader('getresize', '../Lib/resize.py').load_module()

    urls = [
        "/en/homes/buying-a-home/money-timeline-when-buying-property-england-wales-n-ireland",
        "/cy/homes/buying-a-home/money-timeline-when-buying-property-england-wales-n-ireland"
    ]

    for url in urls:

        iterationUrl = "{baseUrl}{url}".format(baseUrl=baseUrl, url=url)
        print('\nVisiting {}'.format(iterationUrl))
        driver.get(iterationUrl)
    
        resize.resizeDesktop(driver)
        print('- Testing dominant callout')
        dominant_callout = driver.find_element(By.CSS_SELECTOR, 'div.cmp-call-out-box--dominant-tool')
        assert dominant_callout.value_of_css_property('margin-top') == "35px"
        assert dominant_callout.value_of_css_property('margin-bottom') == "21px"
        assert dominant_callout.value_of_css_property('padding') == "21px 0px 0px"
        dominant_callout_wrapper = dominant_callout.find_element(By.CSS_SELECTOR, 'div.cmp-call-out-box__wrapper')
        assert dominant_callout_wrapper.value_of_css_property('border-width') == "8px"
        assert "240, 240, 90" in dominant_callout_wrapper.value_of_css_property('border-color')
        dominant_callout_title = dominant_callout_wrapper.find_element(By.CSS_SELECTOR, 'div.cmp-call-out-box__content-main-title > h3')
        assert dominant_callout_title.value_of_css_property('font-size') == "32px"
        assert dominant_callout_title.value_of_css_property('font-weight') == "700"
        assert "0, 11, 59" in dominant_callout_title.value_of_css_property('color')
        assert dominant_callout_title.value_of_css_property('line-height') == "39px"
        print(' - Desktop Dominant callout styles ok')

        resize.resizeMobile(driver)
        dominant_callout = driver.find_element(By.CSS_SELECTOR, 'div.cmp-call-out-box--dominant-tool')
        dominant_callout_title = dominant_callout_wrapper.find_element(By.CSS_SELECTOR, 'div.cmp-call-out-box__content-main-title > h3')
        assert dominant_callout_title.value_of_css_property('font-size') == "25px"
        assert dominant_callout_title.value_of_css_property('line-height') == "33px"
        print(dominant_callout_title.value_of_css_property('line-height'))
        print(' - Mobile Dominant callout styles ok')

        resize.resizeDesktop(driver)

        print('- Testing branch callout external multi links')
        # Get all branch callouts 
        branchCallouts = driver.find_elements(By.CSS_SELECTOR, '.cmp-call-out-box--branch')
        # Get the external links
        externalLink = branchCallouts[0].find_elements(By.CSS_SELECTOR, 'a[data-link-type="external"]')
        
        # Set the expected text based on language
        if "/en/" in iterationUrl:
            expectedText = "(Opens in a new window)"
            print('- Article is English')
            print('- Expected text {}'.format(expectedText))
        elif "/cy/" in iterationUrl:
            expectedText = "Yn agor mewn ffenestr newydd"
            print('- Article is Welsh')
            print('- Expected text {}'.format(expectedText))

        # If the callount contains external links
        if len(externalLink) > 0:

            for link in externalLink:
                # Try and find the spans containing the hidden text
                try:
                    linkSpan = link.find_element(By.CSS_SELECTOR, 'span.sr-only')
                    spanText = linkSpan.text

                    assert spanText == expectedText
                    print('- External Multi link in branch includes the correct hidden text')
                except:
                    message = "\n> BRANCH CALLOUT: {iterationUrl}\n  > WARNING: The external multi links are missing the hidden spans".format(
                        iterationUrl=iterationUrl
                    )
                    print(message)

        else:
            print('- Branch callout does not/no longer contains any external links')
            message = "\n> BRANCH CALLOUT: {iterationUrl}\n  - Branch callout does not/no longer contains any external links".format(
                iterationUrl=iterationUrl
            )
            print(message)

        print("5123 - All callouts should be <ASIDE>s or use aria-role='complementary'")
        callout_selector = "div.cmp-call-out-box"
        callouts = driver.find_elements(By.CSS_SELECTOR, callout_selector)
        for callout in callouts:
            assert callout.get_attribute('role') == "complementary"
