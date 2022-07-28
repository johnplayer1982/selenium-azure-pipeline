from selenium.webdriver.common.by import By
from importlib.machinery import SourceFileLoader
import time

def runTest(baseUrl, driver):

    dismisscookie = SourceFileLoader('getcookiefile', '../Lib/dismisscookie.py').load_module()
    resize = SourceFileLoader('getresize', '../Lib/resize.py').load_module()

    print('\n- Checking Seperator Anchor properties')
    seperator_anchor_page = "{}/en/money-troubles/way-forward/bill-prioritiser".format(baseUrl)

    driver.get(seperator_anchor_page)
    resize.resizeDesktop(driver)
    dismisscookie.dismissCookieBanner(driver)

    seperator_anchor_container = driver.find_element(By.CSS_SELECTOR, 'div.separatoranchor')
    seperator_anchor_element = seperator_anchor_container.find_element(By.CSS_SELECTOR, 'div.cmp-separatoranchor')
    assert seperator_anchor_element.value_of_css_property('margin') == "35px 0px 0px"
    assert seperator_anchor_element.value_of_css_property('padding') == "0px 0px 35px"
    print(' + Element styles OK')

    seperator_anchor_content = seperator_anchor_container.find_element(By.CSS_SELECTOR, 'div.cmp-separatoranchor__content-main-text p')
    assert seperator_anchor_content.value_of_css_property('text-align') == "center"
    assert seperator_anchor_content.value_of_css_property('margin') == "0px"
    print(' + Text styles OK')

    seperator_anchor_line = seperator_anchor_container.find_element(By.CSS_SELECTOR, 'div.cmp-separatoranchor__content-main-text-line')
    assert seperator_anchor_line.value_of_css_property('border-bottom') == "1px solid rgb(229, 229, 229)"
    assert seperator_anchor_line.value_of_css_property('align-items') == "center"
    print(' + Horizontal line styles OK')

    seperator_anchor_button = seperator_anchor_container.find_element(By.CSS_SELECTOR, 'div.cmp-separatoranchor__content-main-text-button')
    assert seperator_anchor_button.value_of_css_property('position') == "absolute"
    assert seperator_anchor_button.value_of_css_property('justify-content') == "center"
    assert seperator_anchor_button.value_of_css_property('bottom') == "-30px"
    assert seperator_anchor_button.value_of_css_property('border-radius') == "50%"
    print(' + Button styles OK')

    seperator_anchor_button_a = seperator_anchor_button.find_element(By.CSS_SELECTOR, 'a.cmp-separatoranchor__content-main-text-button-a')
    assert seperator_anchor_button_a.value_of_css_property('border') == "10px solid rgb(255, 255, 255)"
    assert "174, 0, 96" in seperator_anchor_button_a.value_of_css_property('color')
    print(' + Button a tag styles OK')

    seperator_anchor_button_span = seperator_anchor_button_a.find_element(By.CSS_SELECTOR, 'span.cmp-separatoranchor__content-main-text-button-a-content')
    assert seperator_anchor_button_span.value_of_css_property('padding') == "8.5px 12px"
    assert seperator_anchor_button_span.value_of_css_property('display') == "flex"
    assert seperator_anchor_button_span.value_of_css_property('box-shadow') == "rgba(0, 11, 59, 0.25) 0px 3px 0px 0px"
    assert "255, 255, 255" in seperator_anchor_button_span.value_of_css_property('background-color')
    assert "200, 42, 135" in seperator_anchor_button_span.value_of_css_property('color')
    print(' + Button span tag styles OK')

    seperator_anchor_button_a.click()
    print(' + Clicked anchor button')
    time.sleep(1)
    assert driver.find_element(By.CSS_SELECTOR, 'h2.cmp-section-hero__content-main-text-title').is_displayed()
    print(' + Anchor target element visible')
