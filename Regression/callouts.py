from xml import dom
from selenium.webdriver.common.by import By
from importlib.machinery import SourceFileLoader

def runTest(baseUrl, driver):
    
    urls = [
        "/en/everyday-money/types-of-credit/simple-guide-to-credit-cards",
        "/cy/everyday-money/types-of-credit/simple-guide-to-credit-cards"
    ]

    for url in urls:

        iterationUrl = "{baseUrl}{url}".format(baseUrl=baseUrl, url=url)
        print('\nVisiting {}'.format(iterationUrl))
        driver.get(iterationUrl)
    
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
        print(' - Dominant callout styles ok')

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