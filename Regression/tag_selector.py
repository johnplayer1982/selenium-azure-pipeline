from selenium.webdriver.common.by import By
from importlib.machinery import SourceFileLoader
import random, time

def runTest(baseUrl, driver):
    
    resize = SourceFileLoader('getresize', '../Lib/resize.py').load_module()

    tag_selector_page = "{}/en/money-troubles/way-forward/bill-prioritiser".format(baseUrl)
    driver.get(tag_selector_page)
    resize.resizeDesktop(driver)

    tag_selector_container = driver.find_element(By.CSS_SELECTOR, 'div.bills-payments-tags-selector')
    tag_selector_section = tag_selector_container.find_element(By.CSS_SELECTOR, 'section.cmp-bills-payments-tags-selector')
    assert tag_selector_section.value_of_css_property('padding') == "25px 24px 37px"
    assert tag_selector_section.value_of_css_property('margin') == "35px 0px 0px"
    print(' + Section styles OK')

    tag_selector_back_btn = tag_selector_container.find_element(By.CSS_SELECTOR, 'button.cmp-bills-payments-tags-selector__back-btn')
    assert not tag_selector_back_btn.is_displayed()
    print(' + Back button not initially displayed')

    tag_selector_back_btn_icon = tag_selector_back_btn.find_element(By.CSS_SELECTOR, 'span.cmp-bills-payments-tags-selector__back-btn-icon')
    assert tag_selector_back_btn_icon.get_attribute('aria-hidden') == "true"
    print(' + Back button has correct aria-hidden attribute')

    tag_selector_menu = tag_selector_container.find_element(By.CSS_SELECTOR, 'div.cmp-bills-payments-tags-selector__selector-menu')
    assert tag_selector_menu.value_of_css_property('display') == "block"
    print(' + Menu container visible')

    tag_selector_menu_primary = tag_selector_container.find_element(By.CSS_SELECTOR, 'div.cmp-bills-payments-tags-selector__selector-menu-primary')
    assert tag_selector_menu_primary.value_of_css_property('margin') == "0px -8px 49px"
    assert tag_selector_menu_primary.value_of_css_property('display') == "flex"
    assert tag_selector_menu_primary.value_of_css_property('flex-wrap') == "wrap"
    print(' + Primary menu container styles OK')

    tag_selector_menu_titles = tag_selector_container.find_elements(By.CSS_SELECTOR, 'div.cmp-bills-payments-tags-selector__selector-menu-title h3')
    assert tag_selector_menu_titles[0].value_of_css_property('font-family') == "Roobert, sans-serif"
    assert tag_selector_menu_titles[0].value_of_css_property('font-weight') == "700"
    assert tag_selector_menu_titles[0].value_of_css_property('font-size') == "27px"
    assert tag_selector_menu_titles[0].value_of_css_property('line-height') == "34px"
    assert tag_selector_menu_titles[0].value_of_css_property('margin') == "0px 16px 20px 8px"
    print(' + Step 1 title styles OK')

    # Step 1 buttons

    tag_selector_action_btn = tag_selector_container.find_element(By.CSS_SELECTOR, 'button#selection-action')
    assert tag_selector_action_btn.get_attribute('disabled') == "true"
    print(' + Proceed button disabled by default')

    tag_selector_step_1_buttons = tag_selector_menu_primary.find_elements(By.CSS_SELECTOR, 'button.cmp-bills-payments-tags-selector__button')
    tag_selector_step_1_buttons_count = len(tag_selector_step_1_buttons)
    print(' + {} buttons found on step 1'.format(tag_selector_step_1_buttons_count))

    random_btn_1 = tag_selector_step_1_buttons[random.randrange(0, tag_selector_step_1_buttons_count)]
    random_btn_2 = tag_selector_step_1_buttons[random.randrange(0, tag_selector_step_1_buttons_count)]
    random_btn_3 = tag_selector_step_1_buttons[random.randrange(0, tag_selector_step_1_buttons_count)]
    print(' + Selected some random buttons')

    random_btn_1.click()
    random_btn_2.click()
    random_btn_3.click()
    print(' + 3 options clicked')

    step_1_proceed = tag_selector_container.find_element(By.CSS_SELECTOR, 'button#selection-action')
    step_1_proceed.click()
    print(' + Clicked the next button')

    step_1_heading = tag_selector_container.find_element(By.CSS_SELECTOR, 'h3.cmp-bills-payments-tags-selector__selector-menu-title--step-1')
    assert step_1_heading.value_of_css_property('display') == "none"
    print(' + Step 1 hidden')

    step_2_heading = tag_selector_container.find_element(By.CSS_SELECTOR, 'h3.cmp-bills-payments-tags-selector__selector-menu-title--step-2')
    assert step_2_heading.is_displayed()
    print(' + Step 2 heading displayed')

    disabled_buttons = tag_selector_container.find_elements(By.CSS_SELECTOR, '.cmp-bills-payments-tags-selector__button.is-selected')
    for button in disabled_buttons:
        assert button.get_attribute('disabled') == "true"
    print(' + Buttons from previous step are disabled')

    step_2_menu = tag_selector_container.find_element(By.CSS_SELECTOR, 'div.cmp-bills-payments-tags-selector__selector-menu-important')
    step_2_menu_btns = step_2_menu.find_elements(By.CSS_SELECTOR, 'button.cmp-bills-payments-tags-selector__button')
    step_2_menu_btn_count = len(step_2_menu_btns)
    assert step_2_menu_btn_count > 0
    print(' + One or more step 2 buttons visible')

    time.sleep(3)
    try:
        if step_2_menu_btn_count == 1:
            random_step_2_btn = step_2_menu_btns[0]
        else:
            random_step_2_btn = step_2_menu_btns[random.randrange(0, step_2_menu_btn_count)]
        random_step_2_btn.click()
        print(' + Step 2 option clicked')
    except:
        print(' + Step 2 button not clicked but visible')

    step_2_proceed = driver.find_element(By.CSS_SELECTOR, 'button#selection-action')
    step_2_proceed.click()
    print(' + Step 2 proceed button clicked')

    bill_cards = driver.find_elements(By.CSS_SELECTOR, 'section.cmp-billcardgroup')
    total_bill_cards = len(bill_cards)
    visible_bill_cards = []
    hidden_bill_cards = []
    for card in bill_cards:

        if card.get_attribute('style') == "display: block;":
            visible_bill_cards.append(card)
        else:
            hidden_bill_cards.append(card)

    print(' + {} cards found'.format(total_bill_cards))
    print(' + {} cards visible'.format(len(visible_bill_cards)))
    print(' + {} cards hidden'.format(len(hidden_bill_cards)))
    assert len(visible_bill_cards) > 0
    print(' + More than 1 bill card is visible, user has guidance')
