from selenium.webdriver.common.by import By
from importlib.machinery import SourceFileLoader
import time

def runTest(baseUrl, driver, browser):

    print(' - Testing on {}'.format(browser))    
    resize = SourceFileLoader('getresize', '../Lib/resize.py').load_module()

    accordion_carousel_page = "{}/en/money-troubles/way-forward/job-loss".format(baseUrl)
    driver.get(accordion_carousel_page)
    time.sleep(1)
    print(' - Visiting {}'.format(accordion_carousel_page))
    resize.resizeDesktop(driver)

    # Click the anchor to go to the accordion carousel
    anchor = driver.find_element(By.CSS_SELECTOR, 'a.cmp-iconanchor-link[href="#employment-rights"]')
    anchor.click()
    time.sleep(0.5)

    accordion_carousels_containers = driver.find_elements(By.CSS_SELECTOR, 'div.accordioncarousel')
    # Pick 1 to test
    accordion_carousel_container = accordion_carousels_containers[0]

    assert accordion_carousel_container.find_element(By.CSS_SELECTOR, ".cmp-carousel").value_of_css_property('margin-top') == "35px"
    assert accordion_carousel_container.find_element(By.CSS_SELECTOR, '.cmp-accordion-carousel-action-card__start-card').is_displayed()
    print(' - Start card visible')

    # All guidance cards
    guidance_cards = accordion_carousel_container.find_elements(By.CSS_SELECTOR, '.accordion-carousel-action-card')
    assert guidance_cards[0].is_displayed()
    assert guidance_cards[1].is_displayed()
    print(' - First 2 cards visible')
    assert not guidance_cards[2].is_displayed()
    assert not guidance_cards[3].is_displayed()
    assert not guidance_cards[4].is_displayed()
    assert not guidance_cards[5].is_displayed()
    assert not guidance_cards[6].is_displayed()
    assert not guidance_cards[7].is_displayed()
    print(' - Other 6 cards not visible')

    next_btn = accordion_carousel_container.find_element(By.CSS_SELECTOR, '.cmp-carousel__nav-next')
    driver.execute_script("arguments[0].click();", next_btn)
    print(' - Clicked next')
    time.sleep(1)
    assert not guidance_cards[0].is_displayed()
    assert guidance_cards[1].is_displayed()
    assert guidance_cards[2].is_displayed()
    print(' - Cards 2 and visible, card 1 hidden')

    driver.execute_script("arguments[0].click();", next_btn)
    print(' - Clicked next')
    time.sleep(1)
    assert not guidance_cards[0].is_displayed()
    assert not guidance_cards[1].is_displayed()
    assert guidance_cards[2].is_displayed()
    assert guidance_cards[3].is_displayed()

    driver.execute_script("arguments[0].click();", next_btn)
    print(' - Clicked next')
    time.sleep(1)
    assert not guidance_cards[0].is_displayed()
    assert not guidance_cards[1].is_displayed()
    assert not guidance_cards[2].is_displayed()
    assert guidance_cards[3].is_displayed()
    assert guidance_cards[4].is_displayed()

    driver.execute_script("arguments[0].click();", next_btn)
    print(' - Clicked next')
    time.sleep(1)
    assert not guidance_cards[0].is_displayed()
    assert not guidance_cards[1].is_displayed()
    assert not guidance_cards[2].is_displayed()
    assert not guidance_cards[3].is_displayed()
    assert guidance_cards[4].is_displayed()
    assert guidance_cards[5].is_displayed()

    driver.execute_script("arguments[0].click();", next_btn)
    print(' - Clicked next')
    time.sleep(1)
    assert not guidance_cards[0].is_displayed()
    assert not guidance_cards[1].is_displayed()
    assert not guidance_cards[2].is_displayed()
    assert not guidance_cards[3].is_displayed()
    assert not guidance_cards[4].is_displayed()
    assert guidance_cards[5].is_displayed()
    assert guidance_cards[6].is_displayed()

    driver.execute_script("arguments[0].click();", next_btn)
    print(' - Clicked next')
    time.sleep(1)
    assert not guidance_cards[0].is_displayed()
    assert not guidance_cards[1].is_displayed()
    assert not guidance_cards[2].is_displayed()
    assert not guidance_cards[3].is_displayed()
    assert not guidance_cards[4].is_displayed()
    assert not guidance_cards[5].is_displayed()
    assert guidance_cards[6].is_displayed()
    assert guidance_cards[7].is_displayed()

    print(' - All cards visible and hidden when expected')

    resize.resizeMobile(driver)
    time.sleep(1)
    prev_btn = accordion_carousel_container.find_element(By.CSS_SELECTOR, '.cmp-carousel__nav-prev')
    next_btn = accordion_carousel_container.find_element(By.CSS_SELECTOR, '.cmp-carousel__nav-next')
    assert next_btn.value_of_css_property('display') == "none"
    assert prev_btn.value_of_css_property('display') == "none"
    print(' + Previous and next buttons hidden')

    # Accordions
    # Grab the items
    carousel_items = accordion_carousels_containers[0].find_elements(By.CSS_SELECTOR, 'div.cmp-carousel__item')
    # Remove the start and end cards
    carousel_items.pop(0)
    carousel_items.pop(7)

    for item in carousel_items:
        
        item_content = item.find_element(By.CSS_SELECTOR, '.cmp-accordion-carousel-action-card__guidance-card-content')
        assert item_content.get_attribute('style') == "display: none;"
        print(' + Accordion content hidden')

        expand_btn = item.find_element(By.CSS_SELECTOR, '.cmp-accordion-carousel-action-card__guidance-card-heading-mobile')
        driver.execute_script("arguments[0].click();", expand_btn)
        print(' + Expand button clicked')
        time.sleep(1)
        assert item_content.is_displayed()
        print(' + Accordion content visible')

        driver.execute_script("arguments[0].click();", expand_btn)
        print(' + Clicked collapse button')
        time.sleep(1)
        icon = item.find_element(By.CSS_SELECTOR, '.cmp-accordion-carousel-action-card__guidance-card-heading-mobile-title-icon')
        assert "0, 128, 33" in icon.value_of_css_property('color')
        assert icon.value_of_css_property('font-family') == "money-helper-icons, sans-serif"
        print(' + Icon is green tick')
        assert not item_content.is_displayed()
        print(' + Item content not visible')
        time.sleep(1)
