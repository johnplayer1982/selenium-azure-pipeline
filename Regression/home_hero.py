from selenium.webdriver.common.by import By
from importlib.machinery import SourceFileLoader
import time

def runTest(baseUrl, driver):

    resize = SourceFileLoader('getresize', '../Lib/resize.py').load_module()

    locale = {
        "/en": "For free guidance you can trust, we can help.",
        "/cy": "Ar gyfer arweiniad am ddim gallwch ymddiried ynddo, gallwn helpu."
    }

    for key, value in locale.items():
        
        # Start test in desktop view
        resize.resizeDesktop(driver)

        # Visit the page
        iterationUrl = "{baseUrl}{key}".format(baseUrl=baseUrl, key=key)
        driver.get(iterationUrl)
        print("Visiting URL {url}".format(url=iterationUrl))    

        # Check for hero component
        heroComponent = driver.find_element(By.CSS_SELECTOR, ".homepage-hero")
        assert heroComponent
        print("- Hero component found at {iterationUrl}".format(iterationUrl=iterationUrl))
        
        # Check title is correct
        heroTitle = driver.find_element(By.CSS_SELECTOR, ".cmp-homepage-hero__heading").text
        assert heroTitle == value
        print("- Hero title is correct. expected: {value} , actual: {heroTitle}".format(value=value, heroTitle=heroTitle))

        # Find out more link, check if it contains text and a link - 3053
        heroFindOutMore = driver.find_element(By.CSS_SELECTOR, ".cmp-homepage-hero__center-text")
        assert len(heroFindOutMore.text) > 0
        print("- Hero footer link text found: '{heroFindOutMoreText}'".format(heroFindOutMoreText=heroFindOutMore.text))
        
        # ===== SEARCH ===== #

        # Find the search box
        searchInput = driver.find_element(By.CSS_SELECTOR, "#aa-search-input--homepage-hero")
        print("- Search input found for desktop view")
        # Enter some dummy text
        searchInput.send_keys("Testing clear button")
        print("- Enter dummy text into search field")
        # Click the clear button
        driver.find_element(By.CSS_SELECTOR, "#hero-clear-button").click()
        print("- Clicked the clear input button")
        # Confirm the field is now empty
        assert searchInput.get_attribute("value") == ""
        print("- Search field empty, clear button works correctly")
        
        # Confirm auto suggestion works
        # Enter some meaningful text
        if key == "/en":
            searchTerm = "savings"
        else:
            searchTerm = "angladd"
        searchInput.send_keys(searchTerm)
        time.sleep(2)
        print("- Entered term into the search field")
        
        # Find the auto suggestion element
        searchAutoSuggest = driver.find_element(By.CSS_SELECTOR, 'span#algolia-autocomplete-listbox-3')
        
        # Check if the display: block attribute is in the inline styles
        assert "display: block;" in searchAutoSuggest.get_attribute("style")
        print("- Auto suggest menu present (display: block;)")
        
        # Click an option in the list
        if key == "/en":
            driver.find_element_by_xpath("//p[normalize-space()='savings']").click()
        else:
            driver.find_element_by_xpath("//p[normalize-space()='angladd']").click()
        print("- Clicked an option in the auto suggest list")
        
        # Confirm the option is now populated in the input field
        if key == "/en":
            assert searchInput.get_attribute("value") == searchTerm
        else:
            assert searchInput.get_attribute("value") == searchTerm
        print("- Search populated with clicked suggestion")

        # Click the search button
        search_container = driver.find_element(By.CSS_SELECTOR, 'div.cmp-homepage-hero__searchbar-container')
        search_btn = search_container.find_element(By.CSS_SELECTOR, 'button.cmp-search-box__find')
        search_btn.click()
        print("- Search button clicked")

        # Confirm the search results page (Based on the URL)
        expectedResultsUrl = "{baseUrl}{key}/search-results.html?q={searchTerm}".format(baseUrl=baseUrl, key=key, searchTerm=searchTerm)
        assert driver.current_url == expectedResultsUrl
        print("- Expected search results URL correct: {expectedResultsUrl}".format(expectedResultsUrl=expectedResultsUrl))

        # Go back to the homepage
        driver.get(iterationUrl)
        print("- Heading back to the homepage")

        # ===== CATEGORY LINKS ===== #

        # Confirm the correct number of category links
        heroCategories = driver.find_elements(By.CSS_SELECTOR, ".cmp-homepage-hero__link-item")
        assert len(heroCategories) == 8
        print("- 8 Categories link homepage hero links")

        # Make sure the hm gov logo is present
        hmLogo = driver.find_element(By.CSS_SELECTOR, ".cmp-homepage-hero__gov-logo-image")
        assert hmLogo
        print("- HM Gov logo found")

        # ===== Mobile and Tablet ===== #
        driver.set_window_size(723, 900)
        print("- Resized to mobile breakpoint")
        # Confirm search field isnt visible
        assert not driver.find_element(By.CSS_SELECTOR, "#aa-search-input--homepage-hero").is_displayed()
        print("- Search field not visible on mobile")
        
        # Confirm the find out more link isnt visible - added in 3053
        findOutMoreMobile = driver.find_element(By.CSS_SELECTOR, '.cmp-homepage-hero__center-text')
        findOutMoreMobileVisibility = findOutMoreMobile.value_of_css_property("visibility")
        assert findOutMoreMobileVisibility == "hidden"
        print("- Find out more link hidden for mobile users")
