from selenium.webdriver.common.by import By
from importlib.machinery import SourceFileLoader
import time

def confirm_cookies_on_load(driver):
    all_cookies = driver.get_cookies()
    for cookie_dict in all_cookies:
        # For each item in each dictionary    
        for key, value in cookie_dict.items():
            if key == "value":
                assert "necessaryCookies" not in value
                assert "optionalCookies" not in value
    print('- No optional or necessary cookies set on initial load')

def confirm_accepted_cookies(driver):
    all_cookies = driver.get_cookies()
    accepted_cookies_found = False
    for cookie in all_cookies:
        for key, value in cookie.items():
            if isinstance(value, str):
                if '"optionalCookies":{"analytics":"accepted","marketing":"accepted"}' in value:
                    accepted_cookies_found = True
                    print('- Accepted cookies found')
    assert accepted_cookies_found

def confirm_declined_cookies(driver):
    all_cookies = driver.get_cookies()
    declined_passed = False
    for cookie_dict in all_cookies:
        for key, value in cookie_dict.items():
            # Confirm necessary cookies set
            if key == "value":
                if '"optionalCookies":{"analytics":"revoked","marketing":"revoked"}' in value:
                    declined_passed = True
    assert declined_passed
    print('- Correct cookies set for rejected option')

def confirm_analytics_only(driver):
    all_cookies = driver.get_cookies()
    analytics_only_passed = False
    for cookie_dict in all_cookies:
        for key, value in cookie_dict.items():
            if key == "value":
                if '"optionalCookies":{"analytics":"accepted","marketing":"revoked"}' in value:
                    analytics_only_passed = True
    assert analytics_only_passed
    print('- Correct cookies set for analytics only option')

def confirm_marketing_only(driver):
    all_cookies = driver.get_cookies()
    marketing_only_passed = False
    for cookie_dict in all_cookies:
        for key, value in cookie_dict.items():
            if key == "value":
                if '"optionalCookies":{"analytics":"revoked","marketing":"accepted"}' in value:
                    marketing_only_passed = True
    assert marketing_only_passed
    print('- Correct cookies set for marketing only option')

def runTest(baseUrl, driver):

    resize = SourceFileLoader('getresize', '../Lib/resize.py').load_module()

    driver.get(baseUrl)
    resize.resizeDesktop(driver)
    confirm_cookies_on_load(driver)

    time.sleep(1)
    # Overlay
    overlay = driver.find_element(By.CSS_SELECTOR, 'div#ccc-overlay')
    overlay_opacity = overlay.value_of_css_property('opacity')
    assert overlay_opacity == "1"
    print('- Overlay visible')

    # Top panel
    cookie_panel_top = driver.find_element(By.CSS_SELECTOR, 'div.ccc-notify__top')
    cookie_panel_top_opacity = cookie_panel_top.value_of_css_property('opacity')
    # 5152 - Confirm cookie banner title is H2
    assert driver.find_element(By.CSS_SELECTOR, 'div#ccc-notify-title > h2')
    print('- Cookie preferences top panel title is a H2')
    assert cookie_panel_top.is_displayed()
    assert cookie_panel_top_opacity == "1"
    print("- Cookie preferences top panel visible")

    # Title
    cookie_panel_title_selector = '#ccc-notify-title > h2'
    cookie_panel_title = cookie_panel_top.find_element(By.CSS_SELECTOR, cookie_panel_title_selector)
    cookie_panel_title_styles = {
        "padding" : "0px",
        "margin" : "0px",
        "font-size" : "22px",
        "font-weight" : "700",
        "line-height" : "28px",
    }
    for key, value in cookie_panel_title_styles.items():
        assert cookie_panel_title.value_of_css_property(key) == value
    assert "0, 11, 59" in cookie_panel_title.value_of_css_property('color')
    print('- Top panel title styles ok (h2)')

    # Gov logo in top panel
    cookie_panel_gov_logo = cookie_panel_top.find_element(By.CSS_SELECTOR, '.ccc-notify-text img')
    assert cookie_panel_gov_logo
    print('- Gov logo found')
    assert "logos/logo-en-footer-gov.svg" in cookie_panel_gov_logo.get_attribute("src")
    print('- Gov logo includes correct image in src (logos/logo-en-footer-gov.svg)')

    # Buttons
    cookie_panel_buttons = cookie_panel_top.find_element(By.CSS_SELECTOR, 'div.ccc-notify-buttons')

    # Accept
    accept = cookie_panel_buttons.find_element(By.CSS_SELECTOR, 'button#ccc-notify-accept')
    accept_styles = {
        "margin" : "28px 8px 16px 0px",
        "padding" : "8px 16px",
        "font-size" : "16px",
        "border-radius" : "4px"
    }

    for key, value in accept_styles.items():
        assert accept.value_of_css_property(key) == value
    assert "23" in accept.value_of_css_property('line-height')
    assert "255, 255, 255" in accept.value_of_css_property('color')
    assert "200, 42, 135" in accept.value_of_css_property('background-color')
    assert "255, 255, 255" in accept.find_element(By.CSS_SELECTOR, 'span').value_of_css_property('color')
    print('- Accept button styles OK')

    # Reject
    reject = cookie_panel_buttons.find_element(By.CSS_SELECTOR, 'button#ccc-notify-reject')
    reject_styles = {
        "margin" : "28px 8px 16px 0px",
        "padding" : "8px 16px",
        "border" : "1px solid rgb(174, 0, 96)",
    }
    for key, value in reject_styles.items():
        assert reject.value_of_css_property(key) == value
    assert "255, 255, 255" in reject.value_of_css_property('color')
    assert "0, 0, 0" in reject.value_of_css_property('background-color')
    assert "23" in reject.value_of_css_property('line-height')
    assert "174, 0, 96" in reject.find_element(By.CSS_SELECTOR, 'span').value_of_css_property('color')
    print('- Reject button styles OK')

    set_preferences_link = cookie_panel_buttons.find_element(By.CSS_SELECTOR, 'button.ccc-notify-link')
    assert set_preferences_link
    print('- Set preferences link found')

    set_preferences_link_styles = {
        "margin" : "28px 8px 16px 0px",
        "padding" : "8px 16px",
        "font-weight" : "400",
        "line-height" : "24px",
        "border" : "0px none rgb(255, 255, 255)",
        "font-size" : "16px"
    }

    for key, value in set_preferences_link_styles.items():
        assert set_preferences_link.value_of_css_property(key) == value
    assert "200, 42, 135" in set_preferences_link.find_element(By.CSS_SELECTOR, 'span').value_of_css_property('color')
    print('- Set preferences link styles OK')

    # Click set preferences
    set_preferences_link.click()
    time.sleep(1)

    overlay = driver.find_element(By.CSS_SELECTOR, 'div#ccc-overlay')
    overlay_opacity = overlay.value_of_css_property('opacity')
    assert overlay_opacity == "1"
    print('- Overlay still visible')

    side_menu = driver.find_element(By.CSS_SELECTOR, 'div#ccc-module')

    side_menu_styles = {
        "position" : "fixed",
        "left" : "0px",
        "top" : "0px",
        "bottom" : "0px",
        "max-width" : "520px"
    }

    for key, value in side_menu_styles.items():
        assert side_menu.value_of_css_property(key) == value
    print('- Side menu container styles OK')

    # Check titles are correct levels
    assert side_menu.find_element(By.CSS_SELECTOR, 'div#ccc-title > h2')
    print('- Side menu main title is H2')
    assert side_menu.find_element(By.CSS_SELECTOR, 'div#ccc-necessary-title > h2')
    print('- Side menu neccessary cookies title is H2')
    optional_cookie_headers = side_menu.find_elements(By.CSS_SELECTOR, 'div.optional-cookie-header > h3')
    assert len(optional_cookie_headers) == 2
    print('- 2 Level 3 headings found')

    side_menu_styles = {
        "position" : "fixed",
        "left" : "0px",
        "top" : "0px",
        "bottom" : "0px",
        "max-width" : "520px"
    }

    for key, value in side_menu_styles.items():
        assert side_menu.value_of_css_property(key) == value
    print('- Side menu container styles OK')

    # Cookie functionality
    # On accept, following cookies are set: _gid, _ga_GSRBL25VV8. _fbp, _ga
    accept_btn = side_menu.find_element(By.CSS_SELECTOR, 'button#ccc-recommended-settings')
    accept_btn.click()
    print('- Click accept all cookies')
    time.sleep(1)
    confirm_accepted_cookies(driver)

    # Reopen the menu
    driver.find_element(By.CSS_SELECTOR, 'a.cmp-footer__link-cookie--panel').click()
    time.sleep(1)

    # Reject all cookies
    side_menu = driver.find_element(By.CSS_SELECTOR, 'div#ccc-module')
    reject_btn = side_menu.find_element(By.CSS_SELECTOR, 'button#ccc-reject-settings')
    reject_btn.click()
    print('- Clicked reject cookies')
    confirm_declined_cookies(driver)    

    # Enable analytics cookies only
    driver.find_element(By.CSS_SELECTOR, 'a.cmp-footer__link-cookie--panel').click()
    time.sleep(1)
    side_menu = driver.find_element(By.CSS_SELECTOR, 'div#ccc-module')
    analytics_toggle = side_menu.find_element(By.CSS_SELECTOR, 'span#analytics')
    analytics_toggle.click()
    save_btn = side_menu.find_element(By.CSS_SELECTOR, 'button#ccc-dismiss-button')
    save_btn.click()
    print('- Set analytics cookies only')
    confirm_analytics_only(driver)

    # Marketing cookies only
    driver.find_element(By.CSS_SELECTOR, 'a.cmp-footer__link-cookie--panel').click()
    time.sleep(1)
    side_menu = driver.find_element(By.CSS_SELECTOR, 'div#ccc-module')
    analytics_toggle = side_menu.find_element(By.CSS_SELECTOR, 'span#analytics')
    analytics_toggle.click()

    markting_toggle = side_menu.find_element(By.CSS_SELECTOR, 'span#marketing')
    markting_toggle.click()
    save_btn = side_menu.find_element(By.CSS_SELECTOR, 'button#ccc-dismiss-button')
    save_btn.click()
    print('- Set marketing cookies only')
    confirm_marketing_only(driver)

    print('5480 - Addition of survey A/B test cookie into allow list (no release required)')
    expected_cookie = '"abtest"'
    expected_cookie_found = False
    all_cookies = driver.get_cookies()
    for cookie in all_cookies:
        for key, value in cookie.items():
            if isinstance(value, str):
                if expected_cookie in value:
                    expected_cookie_found = True
    assert expected_cookie_found == True
    print(' - A/B Test cookie found')
