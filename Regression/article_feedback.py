from selenium.webdriver.common.by import By
from importlib.machinery import SourceFileLoader

def runTest(baseUrl, driver):

    dismisscookie = SourceFileLoader('getcookiefile', '../Lib/dismisscookie.py').load_module()
    articlelist = SourceFileLoader('getarticlelist', '../Lib/article_list.py').load_module()
    resize = SourceFileLoader('getresize', '../Lib/resize.py').load_module()
    
    urls = articlelist.get_articles()
    for url in urls:
        iterationUrl = "{baseUrl}{url}".format(baseUrl=baseUrl, url=url)
        driver.get(iterationUrl)
        dismisscookie.dismissCookieBanner(driver)
        print("\nVisiting {iterationUrl}".format(iterationUrl=iterationUrl))
        resize.resizeDesktop(driver)
        print("- Maximising window")

        # Check for the feedback component
        feedbackElem = driver.find_element(By.CSS_SELECTOR, ".cmp-voting")
        assert feedbackElem
        print("- Feedback component found")
        
        # Ensure the panel isnt visible
        hiddenMessageContainer = driver.find_element(By.CSS_SELECTOR, ".cmp-voting__container.cmp-voting__message.hide")
        assert hiddenMessageContainer
        print("- Message hidden on load")
        
        # Click the thumbs up button
        thumbsUpBtn = driver.find_element(By.CSS_SELECTOR, ".cmp-voting__thumb-up")
        driver.execute_script("arguments[0].click();", thumbsUpBtn)
        print("- Thumbs up button clicked")

        # Confirm the message is displayed
        displayedMessageContainer = driver.find_element(By.CSS_SELECTOR, ".cmp-voting__container.cmp-voting__message")
        assert displayedMessageContainer
        print("- Thankyou message displayed")
        
        # Confirm the message has the aria role - Ticket 3148
        feedbackMessage = driver.find_element(By.CSS_SELECTOR, ".cmp-voting__message-feedback")
        assert feedbackMessage.get_attribute("role") == "status"
        print("- Displayed message has the expected role='status' attribute")
        
        # And the buttons are hidden
        thumbContainer = driver.find_element(By.CSS_SELECTOR, ".cmp-voting__container.cmp-voting__vote.hide")
        assert thumbContainer
        print("- Thumb buttons hidden")
