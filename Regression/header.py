from email.mime import base
from selenium.webdriver.common.by import By
from importlib.machinery import SourceFileLoader
import time

def runTest(baseUrl, driver):

    resize = SourceFileLoader('getresize', '../Lib/resize.py').load_module()

    localeUrls = {
        "/en": "Free and impartial help with money, backed by the government | MoneyHelper",
        "/cy": "Cymorth am ddim a diduedd gydag arian, wedi’i gefnogi gan y llywodraeth | HelpwrArian"
    }

    for key, value in localeUrls.items():

        # Start test in desktop view
        resize.resizeDesktop(driver)

        # Define our common values
        iterationUrl = "{baseUrl}{key}".format(baseUrl=baseUrl, key=key)
        print("Visiting URL {url}".format(url=iterationUrl))
        logoCSSSelector = ".cmp-header__logo-desktop"

        # Visit the page
        driver.get(iterationUrl)
        print("- Page title for {key} is {value}".format(key=key, value=value))
        
        # Confirm the page title matches the language
        assert value in driver.title

        # Get the href attribute value 
        hrefLang = driver.find_element(By.CSS_SELECTOR, logoCSSSelector).get_attribute('href')

        assert driver.find_element(By.CSS_SELECTOR, logoCSSSelector)
        print("- Logo element found on page")
        
        # Confirm the href of the logo matches the current url
        assert iterationUrl == hrefLang
        print("- Logo link is {logoLink}".format(logoLink=hrefLang))
        
        # Language Switch
        driver.find_element(By.CSS_SELECTOR, ".cmp-language-navigation-type").click()
        print("- Language switched to alternative language")
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, ".cmp-language-navigation-type").click()
        print("- Language switched back again")
        time.sleep(1)
    
        # Check for the search input
        searchField = driver.find_element(By.CSS_SELECTOR, ".aa-input")
        searchButton = driver.find_element(By.CSS_SELECTOR, ".cmp-search-box__find")

        assert searchField
        print("- Search box found")
        searchField.send_keys("Mortgages")
        searchButton.click()
        print("- Search performed")
        driver.get(iterationUrl)
        
        # ====== TABLET ====== #

        # Resize the window to tablet
        resize.resizeTablet(driver)
        time.sleep(1)
        print("- Window resized to tablet breakpoint")

        # Confirm the tablet logo exists
        tabletLogo = driver.find_element(By.CSS_SELECTOR, ".cmp-header__logo-tablet")

        assert tabletLogo
        print("- Tablet logo found for {key}".format(key=key))
        
        tabletMenuButton = driver.find_element(By.CSS_SELECTOR, ".cmp-header__menu-toggle-open")
        tabletMenuButton.click()
        print("- Mobile menu button clicked")
        driver.find_element(By.CSS_SELECTOR, ".cmp-header__menu--mobile-wrapper")
        print("- Mobile menu opened")
        tabletMenuClose = driver.find_element(By.CSS_SELECTOR, ".cmp-header__menu-toggle-close")
        tabletMenuClose.click()
        print("- Mobile menu closed")

        driver.find_element(By.CSS_SELECTOR, ".cmp-header__search-icon").click()
        print("- Clicked on the search icon")
        # Allow a moment for the search panel to open
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, ".cmp-header__search-mobile")
        print("- Search panel open")
        driver.find_element(By.CSS_SELECTOR, ".cmp-header__search-icon.disabled").click()
        print("- Search panel closed")

        # ====== MOBILE ====== #
        resize.resizeMobile(driver)
        print("- Resized to mobile breakpoint")
        
        # Confirm mobile logo present
        driver.find_element(By.CSS_SELECTOR, ".cmp-header__logo-mobile")
        print("- Mobile logo found")

        # 3709 - "menu" word on mobile and tablet welsh header should change to "bwydlen"
        if key == "/cy":
            menuText = driver.find_element(By.CSS_SELECTOR, 'span.cmp-header__menu-toggle-open-title')
            assert "bwydlen" in menuText.text
            print('- Welsh menu button text ok "bwydlen"')

    # Blog template
    iterationUrl = '{}/en/blog/financial-education/moneyhelpers-couch-to-financial-fitness-programme'.format(baseUrl)
    driver.get(iterationUrl)
    
    # Start test in desktop view
    resize.resizeDesktop(driver)

    header_container = driver.find_element(By.CSS_SELECTOR, 'div.cmp-header__wrapper')

    header_container_right = header_container.find_element(By.CSS_SELECTOR, 'div.cmp-header__container--right')
    assert header_container_right.is_displayed()
    print('- Header search container visible ')

    language_switch = header_container_right.find_element(By.CSS_SELECTOR, 'div.cmp-language-navigation a')
    assert language_switch
    print('- Language switch link found')
    
    # Make sure no-js menu is hidden
    header_search_icon = header_container.find_element(By.CSS_SELECTOR, 'button.cmp-header__search-icon')
    assert header_search_icon.value_of_css_property('display') == "none"
    print('- No js search menu mobile icon hidden')

    # no js menu
    no_js_toggle = header_container.find_element(By.CSS_SELECTOR, 'button.cmp-header__menu-toggle-open')
    assert no_js_toggle.value_of_css_property('display') == "none"
    print('- No js toggle button hidden')

    no_js_menu = header_container.find_element(By.CSS_SELECTOR, 'nav.cmp-header__navigation-no-js')
    search_no_js_menu = no_js_menu.find_element(By.CSS_SELECTOR, 'div.cmp-header__search-mobile-no-js')
    assert search_no_js_menu.value_of_css_property('display') == "none"
    print('- No js search menu hidden')
