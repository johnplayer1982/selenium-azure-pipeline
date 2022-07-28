from selenium.webdriver.common.by import By
from importlib.machinery import SourceFileLoader

def runTest(baseUrl, driver):

    resize = SourceFileLoader('getresize', '../Lib/resize.py').load_module()
    overview_card_page = "{}/en/money-troubles/way-forward".format(baseUrl)

    # Overview card
    driver.get(overview_card_page)
    resize.resizeDesktop(driver)
    print('\n- Overview card')
    # Get overview cards
    overview_cards = driver.find_elements(By.CSS_SELECTOR, '.overview-card')

    for card in overview_cards:

        overview_element = card.find_element(By.CSS_SELECTOR, 'div.cmp-overview-card')
        assert overview_element.value_of_css_property('margin') == "35px 0px 0px"
        print(' + Component top margin OK')

        overview_wrapper = card.find_element(By.CSS_SELECTOR, 'div.cmp-overview-card__wrapper')
        assert overview_wrapper.value_of_css_property('border-radius') == "0px 0px 0px 36px"
        print(' + Component border radius OK')

        overview_image_container = card.find_element(By.CSS_SELECTOR, '.cmp-overview-card__aspect-ratio-container')
        assert overview_image_container.value_of_css_property('position') == "relative"
        assert overview_image_container.value_of_css_property('height') == "0px"
        assert overview_image_container.value_of_css_property('overflow') == "hidden"
        print(' + Image container styles OK')

        overview_image = card.find_element(By.CSS_SELECTOR, 'img.cmp-overview-card__aspect-ratio-asset')
        assert overview_image.value_of_css_property('position') == "absolute"
        assert overview_image.value_of_css_property('top') == "0px"
        assert overview_image.value_of_css_property('object-fit') == "cover"
        print(' + Image styles OK')

        overview_text_container = card.find_element(By.CSS_SELECTOR, 'div.cmp-overview-card__content-main-text')
        assert overview_text_container.value_of_css_property('padding') == "25px 24px 0px"
        assert overview_text_container.value_of_css_property('line-height') == "23px"
        assert overview_text_container.value_of_css_property('display') == "block"
        assert "0, 11, 59" in overview_text_container.value_of_css_property('color')
        print(' + Text container styles OK')

        overview_title = card.find_element(By.CSS_SELECTOR, 'h2.cmp-overview-card__content-main-text-title')
        assert overview_title.value_of_css_property('margin') == "0px"
        assert overview_title.value_of_css_property('padding') == "0px 0px 8px"
        assert overview_title.value_of_css_property('font-family') == "Roobert, sans-serif"
        assert overview_title.value_of_css_property('font-size') == "22px"
        assert overview_title.value_of_css_property('font-weight') == "700"
        assert overview_title.value_of_css_property('line-height') == "28px"
        assert "200, 42, 135" in overview_title.value_of_css_property('color')
        print(' + Title styles OK')

        overview_text = card.find_element(By.CSS_SELECTOR, '.cmp-overview-card__content-main-text > p')
        assert overview_text.value_of_css_property('font-family') == "Roobert, sans-serif"
        assert overview_text.value_of_css_property('font-weight') == "400"
        assert overview_text.value_of_css_property('font-size') == "16px"
        assert overview_text.value_of_css_property('line-height') == "23px"
        assert "0, 11, 59" in overview_text.value_of_css_property('color')
        print(' + Text styles OK')

        overview_button_container = card.find_element(By.CSS_SELECTOR, 'div.cmp-overview-card__content-main-text-button')
        assert overview_button_container.value_of_css_property('display') == "flex"
        assert overview_button_container.value_of_css_property('top') == "auto"
        assert overview_button_container.value_of_css_property('padding') == "24px 24px 37px"
        print(' + Button container styles OK')

        overview_button_link = card.find_element(By.CSS_SELECTOR, 'a.cmp-overview-card__content-main-text-button-a')
        assert overview_button_link.value_of_css_property('position') == "relative"
        assert overview_button_link.value_of_css_property('margin') == "0px"
        assert overview_button_link.value_of_css_property('padding') == "0px"
        assert overview_button_link.value_of_css_property('display') == "flex"
        print(' + Button link styles OK')

        overview_button_span = card.find_element(By.CSS_SELECTOR, 'span.cmp-overview-card__content-main-text-button-a-content')
        assert overview_button_span.value_of_css_property('display') == "flex"
        assert overview_button_span.value_of_css_property('border-radius') == "4px"
        assert overview_button_span.value_of_css_property('font-size') == "16px"
        assert overview_button_span.value_of_css_property('line-height') == "23px"
        assert "255, 255, 255" in overview_button_span.value_of_css_property('background-color')
        assert "200, 42, 135" in overview_button_span.value_of_css_property('color')
        print(' + Button span styles OK')

    # Mobile
    resize.resizeMobile(driver)

    overview_wrappers_mobile = card.find_elements(By.CSS_SELECTOR, 'div.cmp-overview-card__wrapper')

    for overview_wrapper_mobile in overview_wrappers_mobile:
        assert overview_wrapper_mobile.value_of_css_property('border-radius') == "4px"
        assert overview_wrapper_mobile.value_of_css_property('box-shadow') == "rgba(0, 11, 59, 0.25) 0px 3px 0px 0px"
        assert overview_wrapper_mobile.value_of_css_property('border') == "1px solid rgb(157, 161, 202)"
        print(' + Mobile styles OK')
