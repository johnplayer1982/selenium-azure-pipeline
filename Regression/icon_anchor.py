from selenium.webdriver.common.by import By
from importlib.machinery import SourceFileLoader
import time

def runTest(baseUrl, driver):

    resize = SourceFileLoader('getresize', '../Lib/resize.py').load_module()

    # ---------- Icon Anchor ---------- #
    print('\n- Checking Icon Anchor properties')
    icon_anchor_page = "{}/en/money-troubles/way-forward/self-employed".format(baseUrl)
    driver.get(icon_anchor_page)
    resize.resizeDesktop(driver)
    
    icon_anchor_container = driver.find_element(By.CSS_SELECTOR, 'div.iconanchor')
    icon_anchor = icon_anchor_container.find_element(By.CSS_SELECTOR, 'div.cmp-iconanchor')
    assert icon_anchor.value_of_css_property('margin') == "35px 0px 0px"
    print(' + Icon anchor element has correct top margin: 35px')
    icon_anchor_link = icon_anchor_container.find_element(By.CSS_SELECTOR, 'a.cmp-iconanchor-link')

    assert icon_anchor_link.value_of_css_property('margin') == "0px"
    assert icon_anchor_link.value_of_css_property('padding') == "12px 16px"
    assert icon_anchor_link.value_of_css_property('border') == "1px solid rgb(200, 42, 135)"
    assert icon_anchor_link.value_of_css_property('box-shadow') == "rgba(0, 11, 59, 0.25) 0px 3px 0px 0px"
    assert icon_anchor_link.value_of_css_property('display') == "flex"
    assert "174, 0, 96" in icon_anchor_link.value_of_css_property('color')
    print(' + Icon anchor link styles ok')

    icon_anchor_link_icon = icon_anchor_container.find_element(By.CSS_SELECTOR, 'span.cmp-iconanchor-link-icon')
    assert icon_anchor_link_icon.get_attribute("aria-hidden") == "true"
    print(' + Icon anchor link icon has correct aria attribute: "aria-hidden"')
    assert icon_anchor_link_icon.value_of_css_property('margin') == "0px 20px 0px 0px"
    assert icon_anchor_link_icon.value_of_css_property('padding') == "10px 0px"
    assert icon_anchor_link_icon.value_of_css_property('line-height') == "60px"
    assert icon_anchor_link_icon.value_of_css_property('font-size') == "75px"
    assert "200, 42, 135" in icon_anchor_link_icon.value_of_css_property('color')
    print(' + Icon anchor link icon styles ok')

    icon_anchor_link_text = icon_anchor_container.find_element(By.CSS_SELECTOR, '.cmp-iconanchor-link-text-content')
    assert icon_anchor_link_text.value_of_css_property('font-size') == "22px"
    assert icon_anchor_link_text.value_of_css_property('font-weight') == "700"
    assert icon_anchor_link_text.value_of_css_property('line-height') == "28px"
    assert "0, 11, 59" in icon_anchor_link_text.value_of_css_property('color')
    print(' + Icon anchor link text styles ok')

    icon_anchor_link_anchor = icon_anchor_container.find_element(By.CSS_SELECTOR, 'span.cmp-iconanchor-link-anchor')
    assert icon_anchor_link_anchor.get_attribute("aria-hidden") == "true"
    assert icon_anchor_link_anchor.value_of_css_property('margin') == "0px 0px 0px 20px"
    assert icon_anchor_link_anchor.value_of_css_property('font-family') == "money-helper-icons, sans-serif"
    assert icon_anchor_link_anchor.value_of_css_property('font-size') == "30px"
    assert "200, 42, 135" in icon_anchor_link_anchor.value_of_css_property('color')
    print(' + Icon anchor icon styles ok')

    icon_anchor_link.click()
    time.sleep(0.5)
    assert driver.find_element(By.CSS_SELECTOR, 'h2.cmp-section-hero__content-main-text-title').is_displayed()
    print(' + Clicking the Icon anchor scrolls to target')
