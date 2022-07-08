from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from importlib.machinery import SourceFileLoader
import time

def scrollDown(driver):
    documentHeight = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, {})".format(documentHeight/2))
    time.sleep(2)
    print("- Scrolling down 50%")

def runTest(baseUrl, driver):

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
        resize.resizeDesktop(driver)
        print("- Maximising window")

        # Check for localnav
        localNavElem = driver.find_elements_by_css_selector(".local-navigation")
        localNavLength = len(localNavElem)
        assert localNavLength == 2
        print("- {localNavLength} Local navigation components found".format(localNavLength=localNavLength))

        # Check if any links are external and open in new window - derived from 4913
        print('- 4913 : Local Navigation: External links issues')
        related_links = driver.find_elements(By.CSS_SELECTOR, 'div.cmp-local-navigation__related-links-section .cmp-local-navigation__link-item')
        if len(related_links) > 0:
            print(' + Related links found')
            external_links = []
            # Filter out the links which open in a new window and add to the external links list above
            for link in related_links:
                try:
                    # If exernal link exists add it to the external_links list
                    external_related_link = link.find_element(By.CSS_SELECTOR, 'span.new-window')
                    external_links.append(link)
                except:
                    print(' + Related link not an external link')
            for link in external_links:
                link_a = link.find_element(By.CSS_SELECTOR, 'a.cmp-local-navigation__link')
                link_a_href = link_a.get_attribute('href')
                link_icon = link.find_element(By.CSS_SELECTOR, 'span.cmp-local-navigation__link-icon')
                link_hidden_text = link.find_element(By.CSS_SELECTOR, 'span.sr-only')
                link_text = link.get_attribute('innerText')
                assert link_a
                print(' + External link contains <a> tag, href present')
                assert ".html" not in link_a_href
                print(' + External link href does not end in .html')
                assert link_icon
                print(' + External link contains icon')
                assert link_hidden_text
                print(' + External link visually hidden text')
                print(' + Link text: {}'.format(link_text))
        else:
            print(' + No related links found')

        # Switch to mobile
        resize.resizeMobile(driver)
        driver.get(iterationUrl)
        print("- Switching to mobile")
        # Confirm mobile local nav appears on scroll
        scrollDown(driver)

        # Confirm the local nav is not initially visible
        assert not driver.find_element_by_css_selector(".cmp-local-navigation__sticky-banner").get_attribute("class") == ".cmp-local-navigation__sticky-banner.show-mobile-banner"
        print("- Sticky mobile local nav not visible on load")
        
        # Find sticky menu
        mobileNavButton = driver.find_element_by_css_selector(".cmp-local-navigation__sticky-banner.show-mobile-banner")
        mobileNavButton.click()
        print("- Found and clicked mobile local nav sticky button")

        # Confirm navigation is open
        mobileNavOpen = driver.find_element_by_css_selector(".cmp-local-navigation.local-nav-open")
        assert mobileNavOpen
        print("- Mobile sticky navigation open")
        
        # Confirm aria-expanded property is updated to true - 3159
        assert mobileNavButton.get_attribute("aria-expanded") == "true"
        print('- Button has the aria-expanded "true" attribute')
        
        # Confirm the live chat button is not clickable when the local nav is open
        contactBtn = driver.find_element(By.CSS_SELECTOR, 'div.cmp-contact')
        print('- Contact button found')

        try:
            driver.find_element(By.CSS_SELECTOR, '.cmp-contact__trigger').click()
            # Close the chat menu
            driver.find_element(By.CSS_SELECTOR, '.cmp-contact__wrapper-cross').click()
            # Refresh the page and scroll down to show local nav
            driver.get(iterationUrl)
            scrollDown(driver)
            mobileNavButton = driver.find_element(By.CSS_SELECTOR, '.cmp-local-navigation__sticky-banner.show-mobile-banner')
            # Open the nav again so we are back to where we were
            mobileNavButton.click()
        except:
            print('- Live chat button not clickable when local nav is open')

        # Close the mobile local nav panel
        # mobileNavButton.click()
        mobileNavButton.click()
        print("- Close button clicked")

        # Confirm aria-expanded property is updated to false when closed - 3159
        assert mobileNavButton.get_attribute("aria-expanded") == "false"
        print('- Button has the aria-expanded "false" attribute')
        
        # Confirm the panel contents are no longer visible
        mobileNavOpen = driver.find_element_by_css_selector(".cmp-local-navigation")
        assert not mobileNavOpen.get_attribute("class") == ".cmp-local-navigation.local-nav-open"
        print("- The mobile local navigation is closed")

        # Scroll to the bottom of the page
        driver.find_element_by_tag_name("html").send_keys(Keys.END)
        print("- Scrolled to bottom of page")
        assert not driver.find_element_by_css_selector(".cmp-local-navigation__sticky-banner").get_attribute("class") == ".cmp-local-navigation__sticky-banner.show-mobile-banner"
        print("- Navigation hidden")
        
        # Scroll to top to confirm the banner is hidden
        driver.find_element_by_tag_name("html").send_keys(Keys.HOME)
        print("- Scrolled to top of page")
        assert not driver.find_element_by_css_selector(".cmp-local-navigation__sticky-banner").get_attribute("class") == ".cmp-local-navigation__sticky-banner.show-mobile-banner"
        print("- Navigation hidden")
        
        # 3687 - Make sure the live chat button is not clickable when the localnav is open
        driver.set_window_size(375, 667)
        driver.get(iterationUrl)
        print('- Resized to small mobile (375x667)')
        print('- Scrolling down to make sure livechat is not clickable when menu open')
        scrollDown(driver)
        mobileNavButton = driver.find_element_by_css_selector(".cmp-local-navigation__sticky-banner.show-mobile-banner")
        mobileNavButton.click()
        liveChatBtn = driver.find_element(By.CSS_SELECTOR, '.cmp-contact__trigger')
        try:
            liveChatBtn.click()
        except:
            print('- Live chat button not clickable when local nav is open')
