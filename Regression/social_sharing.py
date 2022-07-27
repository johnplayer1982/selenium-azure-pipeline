from selenium.webdriver.common.by import By
from importlib.machinery import SourceFileLoader
import time

def runTest(baseUrl, driver):
    
    resize = SourceFileLoader('getresize', '../Lib/resize.py').load_module()
    articlelist = SourceFileLoader('getarticlelist', '../Lib/article_list.py').load_module()

    articles = articlelist.get_articles()

    for article in articles:

        iterationUrl = "{url}{article}".format(url=baseUrl, article=article)
        iterationUrl = iterationUrl.replace(".html", "")
        driver.get(iterationUrl)
        print("\nVisiting {url}".format(url=iterationUrl))

        # Find social sharing component
        socialSharing = driver.find_element_by_css_selector(".sharing")
        if socialSharing:
            print("- Social sharing component found")

            # Get the expected text from worksheet 2 of the spreadsheet
            if "/en/" in iterationUrl:
                title = "Share this article"
                moreOptions = "More options"
                close = "Close"
                shareWith = "Share this with"
                copyLink = "Copy this link"
                copyBtn = "Copy"
                send_email_Btn = "Send email"
                email_btn = "Email"
                print("- Article is English")
            else:
                title = "Rhannu erthygl"
                moreOptions = "Mwy o opsiynau"
                close = "Cau"
                shareWith = "Rhannu hwn gyda"
                copyLink = "Copio’r ddolen yma"
                copyBtn = "Copio"
                send_email_Btn = "Anfon e-bost"
                email_btn = "E-bost"
                print("- Article is Welsh")

            # Check the title
            sharingTitle = driver.find_element_by_css_selector(".cmp-sharing__text").text
            assert sharingTitle == title
            print("- Component title as expected: {title}".format(title=title))

            # Check the more options link
            moreOptionsLink = driver.find_element_by_css_selector(".cmp-sharing__more-options-text")
            # assert moreOptionsLink.text == moreOptions
            # print("- More options link text as expected: {title}".format(title=title))

            # Click the more options link
            moreOptionsLink.click()
            print("- Clicked the more options link")
            time.sleep(0.5)
            
            # Confirm more options panel is open
            moreOptionsPanel = driver.find_element_by_css_selector(".cmp-sharing__expandable-wrapper-social")
            assert moreOptionsPanel.get_attribute("style") == "display: block;"
            print("- More options panel is open")

            # Confirm copy link input contains the current url
            copyInput = driver.find_element_by_css_selector(".cmp-sharing__copy-this-link-textbox-input")
            assert copyInput.get_attribute("value") == iterationUrl
            print("- 'Copy this link' contains current url")

            # Close the menu
            moreOptionsClose = driver.find_element_by_css_selector(".cmp-sharing__expandable-close-link")
            moreOptionsClose.click()
            print("- Close button clicked")
            time.sleep(1)
            assert moreOptionsPanel.get_attribute("style") == "display: none;"
            print("- More options panel closed")

            # Email dropdown
            emailBtn = driver.find_element_by_css_selector("#email-button")
            email_dropdown_button_text = emailBtn.find_element(By.CSS_SELECTOR, 'span.cmp-sharing__button-text').text
            assert email_dropdown_button_text == email_btn
            print('- Email button contains correct text for language: {}'.format(email_dropdown_button_text))
            emailBtn.click()
            print("- Email button clicked")
            time.sleep(2)

            emailDropdown = driver.find_element_by_css_selector(".cmp-sharing__expandable-wrapper-email")
            send_email_button = emailDropdown.find_element(By.CSS_SELECTOR, 'span.cmp-sharing__button-text').text
            assert emailDropdown.get_attribute("style") == "display: block;"
            print("- Email dropdown menu visible")
            assert send_email_button == send_email_Btn
            print('- Send email button text correct for language: {}'.format(send_email_button))

            emailInput = driver.find_element_by_css_selector("#copy-this-link-textbox-email")
            assert emailInput.get_attribute("value") == driver.current_url
            print("- Email input field contains the correct URL")

            emailClose = emailDropdown.find_element_by_css_selector(".cmp-sharing__expandable-close-link")
            emailClose.click()
            time.sleep(0.6)
            assert emailDropdown.get_attribute("style") == "display: none;"
            print("- Email dropdown closed")

        else:
            raise ValueError("- Social sharing component not found on {url}".format(url=iterationUrl))
