from selenium.webdriver.common.by import By
from importlib.machinery import SourceFileLoader
import time

def runTest(baseUrl, driver, browser):

    print(' - Testing on {}'.format(browser))
    dismisscookie = SourceFileLoader('getcookiefile', '../Lib/dismisscookie.py').load_module()
    resize = SourceFileLoader('getresize', '../Lib/resize.py').load_module()

    url = baseUrl
    locale = {
        "/en": "Talk to us live for…",
        "/cy": "Siaradwch â ni yn fyw am..."
    }

    for key, value in locale.items():
        
        # Start test in desktop view
        resize.resizeDesktop(driver)

        # Visit the correct URL for each language
        iterationUrl = "{url}{key}".format(url=url, key=key)
        driver.get(iterationUrl)
        dismisscookie.dismissCookieBanner(driver)
        print("\nVisiting {iterationUrl}".format(iterationUrl=iterationUrl))

        # Confirm the chat opens
        chatBtn = driver.find_element(By.CSS_SELECTOR, ".cmp-contact__trigger")
        chatBtn.click()
        print("- Clicked the chat button for {key}".format(key=key))
        chatPanel = driver.find_element(By.CSS_SELECTOR, ".cmp-contact__content")
        # assert chatPanel.value_of_css_property('display') == "flex"
        assert chatPanel.is_displayed()
        print("- Chat panel is open")
        
        # Confirm clicking the overlay closes the panel
        chatOverlay = driver.find_element(By.CSS_SELECTOR, ".overlay")
        chatOverlay.click()
        print("- Chat panel overlay clicked")
        assert not chatPanel.is_displayed()
        print("- Chat panel is closed after clicking the overlay")

        # Confirm close button works
        chatBtn.click()
        print("- Re-open chat panel to test close button")
        chatClose = driver.find_element(By.CSS_SELECTOR, ".cmp-contact__wrapper-cross")
        chatClose.click()
        print("- Clicked webchat close button")
        assert not chatPanel.is_displayed()
        print("- Chat panel is closed after clicking the close button")
        
        # Re-open the chat menu and make sure correct language displays
        chatBtn.click()
        print("- Re-open chat panel to confirm correct language is displaying")
        chatTitle = driver.find_element(By.CSS_SELECTOR, ".cmp-contact__content-heading").text
        print(chatTitle, value)
        assert value in chatTitle
        print("- Chat title is in correct language ({key})".format(key=key))
        
        # Check menu level 2
        previousBtnCSS = ".cmp-contact__wrapper-previous"
        if key == "/en":
            level1item1 = driver.find_element(By.XPATH, "//div[@class='cmp-contact__content']//span[@class='cmp-contact__menu-item-content'][normalize-space()='Pensions guidance']")
        else:
            level1item1 = driver.find_element(By.XPATH, "//div[@class='cmp-contact__content']//span[@class='cmp-contact__menu-item-content'][normalize-space()='Arweiniad pensiynau']")
        
        level1item1.click()
        print("- Level 1 item 1 clicked")
        driver.find_element(By.CSS_SELECTOR, previousBtnCSS).click()
        print("- Back to level 1")

        if key == "/en":
            level1item2 = driver.find_element(By.XPATH, "//div[@class='cmp-contact__content']//span[@class='cmp-contact__menu-item-content'][normalize-space()='Money guidance']")
        else:
            level1item2 = driver.find_element(By.XPATH, "//div[@class='cmp-contact__content']//span[@class='cmp-contact__menu-item-content'][normalize-space()='Arweiniad ariannol']")

        level1item2.click()
        print("- Level 1 item 2 clicked")
        level2PreviousBtn = driver.find_element(By.CSS_SELECTOR, ".cmp-contact__wrapper-previous")
        level2PreviousBtn.click()
        print("- Back to level 1")

        # Level 3 test
        # We need to keep referencing the elements as they are updated by JS

        # Only check level 3 on production, on test the welsh menu isnt populated
        if url == "https://www.moneyhelper.org.uk":
            if key == "/en":
                level1item1 = driver.find_element(By.XPATH, "//div[@class='cmp-contact__content']//span[@class='cmp-contact__menu-item-content'][normalize-space()='Pensions guidance']")
            else:
                level1item1 = driver.find_element(By.XPATH, "//div[@class='cmp-contact__content']//span[@class='cmp-contact__menu-item-content'][normalize-space()='Arweiniad pensiynau']")
            
            level1item1.click()
            print("- Clicked level 1 item 1")

            driver.find_element(By.XPATH, "//body/div[@id='contact-1to1']/div[@class='cmp-contact__content']/div[@class='scroll-bay']/div[@class='cmp-contact__menu aem-Grid aem-Grid--12']/div[1]/button[1]/span[1]").click()
            driver.find_element(By.CSS_SELECTOR, previousBtnCSS).click()
            print("- Clicked level 2 item 1")
            
            driver.find_element(By.XPATH, "//body/div[@id='contact-1to1']/div[@class='cmp-contact__content']/div[@class='scroll-bay']/div[@class='cmp-contact__menu aem-Grid aem-Grid--12']/div[2]/button[1]/span[1]").click()
            driver.find_element(By.CSS_SELECTOR, previousBtnCSS).click()
            print("- Clicked level 2 item 2")

            driver.find_element(By.XPATH, "//body/div[@id='contact-1to1']/div[@class='cmp-contact__content']/div[@class='scroll-bay']/div[@class='cmp-contact__menu aem-Grid aem-Grid--12']/div[3]/button[1]/span[1]").click()
            driver.find_element(By.CSS_SELECTOR, previousBtnCSS).click()
            print("- Clicked level 2 item 3")

            driver.find_element(By.CSS_SELECTOR, previousBtnCSS).click()
            print("- Going back to level 1")

            driver.find_element(By.CSS_SELECTOR, ".cmp-contact__wrapper-cross").click()
            print("- Closing the menu")
        else:
            driver.find_element(By.CSS_SELECTOR, ".cmp-contact__wrapper-cross").click()
            print("- Closing the menu")

        # Resizing to mobile
        resize.resizeMobile(driver)

        # Get the position of the button
        mobileChatButton = driver.find_element(By.CSS_SELECTOR, ".cmp-contact__trigger")
        # location returns a dictionary with the x and y position
        mobileBtnX = mobileChatButton.location['x']
        mobileBtnY = mobileChatButton.location['y']

    print('5164 - Implement toggle for 1:1 Guidance component in AEM page properties')
    templates = {
        "Article" : "/en/jp-test/ticket-specific/5164---chat-disabled",
        "Blog" : "/en/jp-test/ticket-specific/5164---blog",
        "Single Column" : "/en/jp-test/ticket-specific/5164---single-column",
        "L1 Landing Page" : "/en/jp-test/ticket-specific/5164---l1",
        "L2 Landing Page" : "/en/jp-test/ticket-specific/5164---l2",
        "Tools Page" : "/en/jp-test/ticket-specific/5164---tools",
        "Homepage" : "/en/jp-test/ticket-specific/5164-homepage"
    }
    if "test.moneyhelper" in url:
        for key, value in templates.items():
            print(' - Checking {} template'.format(key))
            driver.get("{url}{value}".format(url=url, value=value))
            chat_menus = driver.find_elements(By.CSS_SELECTOR, 'div.cmp-contact')
            assert len(chat_menus) == 0
            print(' + Livechat not found on page with it disabled')

    ticket = "5083"
    print('{} - Incorrect redirect URLs in Online Web Form'.format(ticket))
    driver.get(url)
    time.sleep(1)
    dismisscookie.dismissCookieBanner(driver)
    resize.resizeDesktop(driver)
    # Pensions Guidance
    contact_btn = driver.find_element(By.CSS_SELECTOR, 'button.cmp-contact__trigger')
    contact_btn.click()
    driver.find_element(By.CSS_SELECTOR, 'button[data-menu="menuPensions"]').click()
    driver.find_element(By.CSS_SELECTOR, 'button[data-menu="webFormPensions"]').click()
    webform_button = driver.find_element(By.CSS_SELECTOR, 'button.cmp-contact__phone-number.cmp-contact__new-window')
    webform_button_link = webform_button.get_attribute('data-web-chat-url')
    assert not ".html" in webform_button_link
    print("Pensions guidance webform link does not contain .html: {}".format(webform_button_link))
    close_btn = driver.find_element(By.CSS_SELECTOR, 'a.cmp-contact__wrapper-cross')
    close_btn.click()
    # Money Guidance
    contact_btn = driver.find_element(By.CSS_SELECTOR, 'button.cmp-contact__trigger')
    contact_btn.click()
    driver.find_element(By.CSS_SELECTOR, 'button[data-menu="menuSomethingElse"]').click()
    driver.find_element(By.CSS_SELECTOR, 'button[data-menu="webFormSomethingElse"]').click()
    webform_button = driver.find_element(By.CSS_SELECTOR, 'button.cmp-contact__phone-number.cmp-contact__new-window')
    webform_button_link = webform_button.get_attribute('data-web-chat-url')
    assert not ".html" in webform_button_link
    print("Money guidance webform link does not contain .html: {}".format(webform_button_link))
    close_btn = driver.find_element(By.CSS_SELECTOR, 'a.cmp-contact__wrapper-cross')
    close_btn.click()
