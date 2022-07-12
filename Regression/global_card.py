from selenium.webdriver.common.by import By
from importlib.machinery import SourceFileLoader

def runTest(baseUrl, driver):

    resize = SourceFileLoader('getresize', '../Lib/resize.py').load_module()

    global_card_page = "{}/en/money-troubles/way-forward".format(baseUrl)
    resize.resizeDesktop(driver)
    driver.get(global_card_page)

    globalcard_container = driver.find_element(By.CSS_SELECTOR, 'div.globalcard')
    globalcard_element = globalcard_container.find_element(By.CSS_SELECTOR, 'div.cmp-globalcard')
    globalcard_element_wrapper = globalcard_container.find_element(By.CSS_SELECTOR, '.cmp-globalcard__wrapper')

    assert globalcard_element_wrapper.value_of_css_property('border') == "1px solid rgb(157, 161, 202)"
    assert globalcard_element_wrapper.value_of_css_property('border-radius') == "0px 0px 0px 36px"
    print(' + Wrapper styles OK (Border and border radius)')

    assert globalcard_element.value_of_css_property('margin-top') == "35px"
    print(' + Component margin OK, 35px top')

    globalcard_image = globalcard_element.find_element(By.CSS_SELECTOR, 'div.cmp-globalcard__image-container')
    assert globalcard_image.value_of_css_property('flex-basis') == "66%"
    assert globalcard_image.value_of_css_property('border-radius') == "0px 0px 0px 36px"
    print(' + Image container styles OK')

    globalcard_overlay_text = globalcard_element.find_element(By.CSS_SELECTOR, '.cmp-globalcard__title-overlay')
    assert globalcard_overlay_text.value_of_css_property('margin') == "0px"
    assert globalcard_overlay_text.value_of_css_property('padding') == "10px 16px"
    assert globalcard_overlay_text.value_of_css_property('color') == "rgba(0, 11, 59, 1)"
    assert globalcard_overlay_text.value_of_css_property('font-size') == "48px"
    assert globalcard_overlay_text.value_of_css_property('font-weight') == "700"
    print(' + Image overlay text styles OK')

    globalcard_text = globalcard_element.find_element(By.CSS_SELECTOR, '.cmp-globalcard__content-main-text')
    assert globalcard_text.value_of_css_property('margin') == "0px"
    assert globalcard_text.value_of_css_property('padding') == "20px 24px 26px"
    assert globalcard_text.value_of_css_property('flex-basis') == "34%"
    print(' + Text container styles OK')

    globalcard_text_title = globalcard_text.find_element(By.CSS_SELECTOR, 'p.cmp-globalcard__content-main-text-title')
    assert globalcard_text_title.value_of_css_property('font-size') == "22px"
    assert globalcard_text_title.value_of_css_property('margin') == "0px 0px 24px"
    assert globalcard_text_title.value_of_css_property('padding') == "0px"
    assert globalcard_text_title.value_of_css_property('font-weight') == "700"
    assert globalcard_text_title.value_of_css_property('font-family') == "Roobert, sans-serif"
    print(' + Text container title OK')

    globalcard_list_items = globalcard_text.find_elements(By.CSS_SELECTOR, '.cmp-globalcard__content-main-text-list-item')
    print(' + Testing list items:')
    for item in globalcard_list_items:
        
        assert item.value_of_css_property('margin') == "0px 0px 24px"
        assert item.value_of_css_property('padding') == "0px"
        assert item.value_of_css_property('line-height') == "28px"
        assert item.value_of_css_property('color') == "rgba(0, 11, 59, 1)"
        assert item.value_of_css_property('display') == "flex"

        # Icons
        icon = item.find_element(By.CSS_SELECTOR, 'span.cmp-globalcard__content-main-text-list-item-icon')
        assert icon.get_attribute('aria-hidden') == "true"

        assert icon.value_of_css_property('color') == "rgba(200, 42, 135, 1)"
        assert icon.value_of_css_property('margin') == "0px 12px 0px 0px"
        assert icon.value_of_css_property('font-size') == "20px"

        # Text
        text = item.find_element(By.CSS_SELECTOR, 'span.cmp-globalcard__content-main-text-list-item-text')
        assert text.value_of_css_property('font-size') == "19px"
        assert text.value_of_css_property('font-family') == "Roobert, sans-serif"
        assert text.value_of_css_property('color') == "rgba(0, 11, 59, 1)"
        assert text.value_of_css_property('margin') == "0px"
        assert text.value_of_css_property('padding') == "0px"

    print(' + List item styles OK')

    # Buttons
    globalcard_button = globalcard_element.find_element(By.CSS_SELECTOR, 'a.cmp-globalcard__content-main-text-button-a')
    assert globalcard_button
    print(' + Button found')
    assert globalcard_button.value_of_css_property('margin') == "0px"
    assert globalcard_button.value_of_css_property('padding') == "0px"
    assert globalcard_button.value_of_css_property('color') == "rgba(174, 0, 96, 1)"
    assert globalcard_button.value_of_css_property('cursor') == "pointer"
    print(' + Button element styles OK')

    globalcard_button_span = globalcard_button.find_element(By.CSS_SELECTOR, 'span.cmp-globalcard__content-main-text-button-a-content')
    assert globalcard_button_span.value_of_css_property('margin') == "0px"
    assert globalcard_button_span.value_of_css_property('padding') == "8.5px 16px"
    assert globalcard_button_span.value_of_css_property('color') == "rgba(255, 255, 255, 1)"
    assert globalcard_button_span.value_of_css_property('background-color') == "rgba(200, 42, 135, 1)"
    assert globalcard_button_span.value_of_css_property('font-size') == "16px"
    assert globalcard_button_span.value_of_css_property('line-height') == "23px"
    print(' + Button element text styles OK')

    # Mobile
    resize.resizeMobile(driver)

    globalcard_image_container = globalcard_container.find_element(By.CSS_SELECTOR, 'div.cmp-globalcard__image-container')
    globalcard_text_container = globalcard_container.find_element(By.CSS_SELECTOR, 'div.cmp-globalcard__content-main-text')
    assert globalcard_image_container.value_of_css_property('flex-basis') == "auto"
    print(' + Global card image has correct flex basis on mobile: auto')
    assert globalcard_text_container.value_of_css_property('display') == "block"
    print(' + Global card text has correct display on mobile: block')
