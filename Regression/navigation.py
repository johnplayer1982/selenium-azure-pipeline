from selenium.webdriver.common.by import By
from importlib.machinery import SourceFileLoader
import time

def runTest(baseUrl, driver):

    resize = SourceFileLoader('getresize', '../Lib/resize.py').load_module()

    locales = [
        "/en",
        "/cy",
    ]

    # Iterate through the urls
    for key in locales:
        
        url = baseUrl

        # Visit the correct language
        iterationUrl = "{url}{key}".format(url=url, key=key)
        print("Visiting URL {url}".format(url=iterationUrl))
        driver.get(iterationUrl)

        print("- Starting Desktop Tests for {key}".format(key=key))

        # Start with the max screen size
        resize.resizeDesktop(driver)
        print("- Maximising window")

        # Get the menu list element
        dTMenuListElem = driver.find_element(By.CSS_SELECTOR, ".cmp-header__menu-list")
        # Store the menu items in a list
        dTMenuList = driver.find_elements(By.CSS_SELECTOR, ".cmp-header__menu-list-item-title")

        # Iterate through the menu items
        for item in dTMenuList:
            # Open the menu
            item.click()
            print("- Opened menu item: {item.text}".format(item=item))
            time.sleep(2)
            print("- Pause for 2 seconds to allow for the classes to be applied")
            # Find the submenu, confirming the submenu has opened
            driver.find_element(By.CSS_SELECTOR, ".cmp-header__submenu")
            print("- Confirmed menu is visible")
            # Close the menu item using the close button
            driver.find_element(By.CSS_SELECTOR, "li[class='cmp-header__menu-list-item focus'] div[class='cmp-header__submenu-close']").click()
            print("- Closed menu item: {item.text}".format(item=item))

        # ====== TABLET ====== # 

        # Resize the window to tablet
        resize.resizeTablet(driver)
        print("- Window resized to tablet breakpoint")

        # Confirm menu button present
        mobileMenuBtn = driver.find_element(By.CSS_SELECTOR, ".cmp-header__menu-toggle-open")
        print("- Mobile menu present")
        # Opening the menu
        mobileMenuBtn.click()
        print("- Clicked mobile menu button")
        # Confirm menu is open
        driver.find_element(By.CSS_SELECTOR, ".cmp-header__menu--mobile-container")
        print("- Menu is open")

        # Save the menu items in a list
        mobileMenuItems = driver.find_elements(By.CSS_SELECTOR, ".cmp-header__menu--mobile-item-btn")

        # Go through the menu items and open/close
        for item in mobileMenuItems:
            item.click()
            print("- Opened menu item {item}".format(item=item.text))
            time.sleep(0.3)
            item.click()
            print("- Closed menu item {item}".format(item=item.text))

            # Verify tools menu has updated style from 3261
            toolsPanel = driver.find_element(By.CSS_SELECTOR, '.cmp-header__submenu--mobile-tools-wrapper')
            # Check the background colout
            toolsPanelBg = toolsPanel.value_of_css_property("background-color")
            assert toolsPanelBg == "rgba(255, 255, 255, 1)"
            print("- Tools panel in menu has white background as expected")

            # Check the border
            toolsPanelBorder = toolsPanel.value_of_css_property("border")
            assert toolsPanelBorder == "1px solid rgb(157, 161, 202)"
            print("- Tools panel has the expected 1px solid border")

        # Check the language switch in the menu
        driver.find_element(By.CSS_SELECTOR, "div[class='cmp-header__menu--mobile-bottom'] a[aria-label='change language']").click()
        time.sleep(2)
        print("- Switching language")
        if key == "/en":
            assert "{url}/cy".format(url=url) in driver.current_url
            print("- URL changed from {key} to /cy".format(key=key))

        elif key == "/cy":
            assert "{url}/en".format(url=url) in driver.current_url
            print("- URL changed from {key} to /en".format(key=key))

        # ====== LANGUAGE SWITCH ====== #
        time.sleep(2)
        # Reopen the menu
        mobileMenuBtn = driver.find_element(By.CSS_SELECTOR, "button.cmp-header__menu-toggle-open").click()

        # Change the language back again
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, "div[class='cmp-header__menu--mobile-bottom'] a[aria-label='change language']").click()
        print("- Language switched back to {key}".format(key=key))

        # ====== OVERLAY DISMISS ====== #

        # Reopen the menu
        time.sleep(2)
        mobileMenuBtn = driver.find_element(By.CSS_SELECTOR, ".cmp-header__menu-toggle-open")
        mobileMenuBtn.click()
        time.sleep(2)
        # Close the menu by clicking on the overlay
        mobileOverlay = driver.find_element(By.CSS_SELECTOR, ".cmp-header__overlay--small-screen")
        mobileOverlay.click()
        # Confirm menu is closed
        # Give the menu a second to finish its animated transition
        time.sleep(1)
        mobileMenuStyle = driver.find_element(By.CSS_SELECTOR, ".cmp-header__menu--mobile-container").get_attribute("style")
        assert mobileMenuStyle == "display: none;"
        print("- Menu closed by clicking the overlay")

    # ----- Current selected menu item 3710 ----- #

    print('- Testing selected state')
    # L1
    l1url = "{}/en/benefits".format(url)
    driver.get(l1url)
    print('- Visited Benefits L1')
    headerItems = driver.find_elements(By.CSS_SELECTOR, 'li.cmp-header__menu-list-item')
    assert "current-page" in headerItems[0].get_attribute("class")
    print('- 1 of 3: Benefits menu item highlighted for benefits L1')
    
    # L2
    l2url = "{}/en/benefits/benefits-if-you-have-children".format(url)
    driver.get(l2url)
    print('- Visited Benefits if you have children L2')
    headerItems = driver.find_elements(By.CSS_SELECTOR, 'li.cmp-header__menu-list-item')
    assert "current-page" in headerItems[0].get_attribute("class")
    print('- 2 of 3: Benefits menu item highlighted for benefits when you have children L2')
    
    # Aritcle
    articleurl = "{}/en/benefits/benefits-if-you-have-children/claiming-child-benefit".format(url)
    driver.get(articleurl)
    print('- Visited Claiming child benefit article page')
    headerItems = driver.find_elements(By.CSS_SELECTOR, 'li.cmp-header__menu-list-item')
    assert "current-page" in headerItems[0].get_attribute("class")
    print('- 3 of 3: Benefits menu item highlighted for child benefit article page')
    
    # 3709 - "menu" word on mobile and tablet welsh header should change to "bwydlen"

    resize.resizeMobile(driver)
    driver.get("{}/cy".format(url))
    expectedCYMenu = "bwydlen"
    menuText = driver.find_element(By.CSS_SELECTOR, 'span.cmp-header__menu-toggle-open-title')
    assert menuText.text == expectedCYMenu
    print('- Welsh menu button text correct: {}'.format(expectedCYMenu))

