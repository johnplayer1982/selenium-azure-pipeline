from selenium.webdriver.common.by import By
from importlib.machinery import SourceFileLoader

def runTest(baseUrl, driver, browser):

    print(' - Testing on {}'.format(browser))
    resize = SourceFileLoader('getresize', '../Lib/resize.py').load_module()

    # ---------- Section Hero ---------- #
    section_hero_page = "{}/en/money-troubles/way-forward/squeezed-income".format(baseUrl)
    driver.get(section_hero_page)
    resize.resizeDesktop(driver)

    section_heros = driver.find_elements(By.CSS_SELECTOR, 'div.section-hero')
    for hero in section_heros:

        section_elem = hero.find_element(By.CSS_SELECTOR, 'div.cmp-section-hero')
        assert section_elem.value_of_css_property('margin-top') == "35px"
        assert section_elem.value_of_css_property('position') == "relative"
        print(' + Section container styles ok')

        section_wrapper = section_elem.find_element(By.CSS_SELECTOR, 'div.cmp-section-hero__wrapper')
        assert section_wrapper.value_of_css_property('padding-top') == "45px"
        assert section_wrapper.value_of_css_property('align-items') == "flex-start"
        print(' + Section wrapper styles OK')

        section_image_container = section_wrapper.find_element(By.CSS_SELECTOR, 'div.cmp-section-hero__image-container')
        assert section_image_container.value_of_css_property('padding') == "55px 28px 0px 40px"
        print(' + Image container styles OK')

        section_image_icon = section_image_container.find_element(By.CSS_SELECTOR, 'span.cmp-section-hero__image-icon')
        assert section_image_icon.value_of_css_property('position') == "relative"
        assert section_image_icon.value_of_css_property('z-index') == "1"
        assert section_image_icon.value_of_css_property('font-size') == "85px"
        print(' + Icon span styles OK')

        section_background_desktop = section_image_container.find_element(By.CSS_SELECTOR, 'svg.cmp-section-hero__image-background--desktop')
        assert section_background_desktop.value_of_css_property('display') == "block"
        assert section_background_desktop.value_of_css_property('fill') == "rgb(15, 25, 160)"
        assert section_background_desktop.value_of_css_property('position') == "absolute"
        assert section_background_desktop.value_of_css_property('left') == "-70px"
        assert section_background_desktop.value_of_css_property('top') == "-35px"
        assert section_background_desktop.value_of_css_property('width') == "223px"
        print(' + Desktop Icon background visible on desktop')
        print(' + Desktop Icon background styles OK')

        section_background_mobie = section_image_container.find_element(By.CSS_SELECTOR, 'svg.cmp-section-hero__image-background--mobile')
        assert section_background_mobie.value_of_css_property('display') == "none"
        print(' + Mobile icon background hidden on desktop')


        section_text_container = section_wrapper.find_element(By.CSS_SELECTOR, 'div.cmp-section-hero__content-main-text')
        assert section_text_container.value_of_css_property('padding') == "0px 0px 0px 55px"
        assert section_text_container.value_of_css_property('margin') == "0px"
        print(' + Text container styles OK')

        section_title = section_text_container.find_element(By.CSS_SELECTOR, 'h2.cmp-section-hero__content-main-text-title')
        assert section_title.value_of_css_property('line-height') == "54px"
        assert section_title.value_of_css_property('font-size') == "48px"
        assert section_title.value_of_css_property('padding') == "0px 0px 35px"
        assert section_title.value_of_css_property('margin') == "0px"
        assert "15, 25, 160" in section_title.value_of_css_property('color')
        print(' + Title styles OK')

        section_text = section_text_container.find_elements(By.CSS_SELECTOR, 'div.cmp-section-hero__content-main-text p')
        for text in section_text:
            assert text.value_of_css_property('margin') == "0px"
            assert text.value_of_css_property('line-height') == "23px"
            assert text.value_of_css_property('font-weight') == "400"
            assert text.value_of_css_property('font-size') == "16px"
            assert "0, 11, 59" in text.value_of_css_property('color')
        print(' + Text styles OK')
