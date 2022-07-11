from email.mime import base
from selenium.webdriver.common.by import By
from importlib.machinery import SourceFileLoader
import time

def runTest(baseUrl, driver):

    resize = SourceFileLoader('getresize', '../Lib/resize.py').load_module()
    searchterms = SourceFileLoader('getsearchterms', '../Lib/search_terms.py').load_module()
    dismisscookie = SourceFileLoader('getcookiefile', '../Lib/dismisscookie.py').load_module()
    siteUrl = "{}/en/search-results.html?q=".format(baseUrl)

    # Start test in desktop view
    resize.resizeDesktop(driver)

    def runSearchTest(term, lang):

        dismisscookie.dismissCookieBanner(driver)
        searchTerm = term
        print("\n- Running Search term test for '{term}'".format(term=searchTerm))

        # Reformat the term to replace the spaces with %2520 as this is what we expect in the url
        searchURL = searchTerm.replace(" ", "%20")

        # Perform the search
        time.sleep(1.5)
        inpage_search = driver.find_element(By.CSS_SELECTOR, 'div.searchbox')
        search_input = inpage_search.find_element(By.CSS_SELECTOR, 'section.cmp-search-box div.cmp-search-box__field input#aa-search-input')
        assert search_input
        search_input.send_keys(searchTerm)
        driver.find_element(By.CSS_SELECTOR, "div.searchbox div.cmp-search-box__field > button.cmp-search-box__find").click()
        print("- Searching for {searchTerm}".format(searchTerm=searchTerm))
    
        # Confirm search has been performed using the URL
        expected_url = "{url}/{lang}/search-results.html?q={term}".format(url=baseUrl, lang=lang, term=searchURL)

        assert driver.current_url == expected_url
        print("- Expect URL: {url}/{lang}/search-results.html?q={term}".format(url=baseUrl, lang=lang, term=searchURL))
        print("- Actual URL: {url}".format(url=driver.current_url))

        # Confirm the search term has been populated into the header search
        assert driver.find_element(By.CSS_SELECTOR, "#aa-search-input--header-desktop").get_attribute('value') == searchTerm
        print("- Search term {term} has been populated into the header search input".format(term=searchTerm))
        
        # Broken in PROD!
        # Wait a moment for the input clear button to display
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, "div.cmp-search-box__field > button.cmp-search-box__find").click()
        print("- Clearing the input")

        # Get each of the results on the 1st page
        searchResults = driver.find_elements(By.CSS_SELECTOR, ".cmp-algolia-results__list li")
        assert len(searchResults) >= 1
        print("- Results are being displayed: {numberOfResults} results on the 1st page for {searchTerm}".format(numberOfResults=len(searchResults), searchTerm=searchTerm))

        if "test.moneyhelper" in baseUrl:
            expectedAttribute = 'article[data-insights-index="crawler_money-and-pensions-service-EN"]'
        else:
            expectedAttribute = 'article[data-insights-index="crawler_money-and-pensions-service-prod-EN"]'

        assert driver.find_element(By.CSS_SELECTOR, expectedAttribute)
        datalayer = driver.execute_script("return window.dataLayer")
        assert "'algoliaUserToken': '" in str(datalayer)
        print(' + Data Insights Index tag found')
        print(' + AlgoliaUserToken found in DataLayer')

    print('+ 4410 - Blog Template Search UI Issues')
    blogpost = "{}/en/blog/scams-and-fraud/how-to-spot-and-avoid-dating-scams".format(baseUrl)
    driver.get(blogpost)
    print('- Navigating to blog post')
    nojs_desktop_search = driver.find_element(By.CSS_SELECTOR, 'div.cmp-header__search-mobile-no-js')
    assert nojs_desktop_search.value_of_css_property('display') == "none"
    print('- No js search box hidden on desktop')
    
    def createURL(lang):
        print("- Creating localised URL en|cy")
        localisedURL = "{url}/{lang}/search-results.html?q=".format(url=baseUrl, lang=lang)
        return localisedURL

    searchterms = searchterms.get_search_terms()

    for term in searchterms:
        lang = "en"
        driver.get(createURL(lang))
        runSearchTest(term, lang)

    # 4852 - Search suggestions not displaying on mobile search
    driver.get(baseUrl)
    print('\n4852 - Search suggestions not displaying on mobile search')
    resize.resizeMobile(driver)
    print('- Resizing to mobile')
    header_elem = driver.find_element(By.CSS_SELECTOR, 'div.header')
    search_icon = header_elem.find_element(By.CSS_SELECTOR, 'button.cmp-header__search-icon')
    search_icon.click()
    print('- Clicked search icon in header')
    time.sleep(1)
    search_panel = header_elem.find_element(By.CSS_SELECTOR, 'div.cmp-header__search-mobile')
    search_input = search_panel.find_element(By.CSS_SELECTOR, 'section.cmp-search-box div.cmp-search-box__field input#aa-search-input--header-mobile')
    search_input.send_keys("housin")
    print('- Entered partial term into search field')
    time.sleep(2)
    print('- Waiting for the suggestions dropdown to appear')
    suggestions = header_elem.find_element(By.CSS_SELECTOR, '.aa-dropdown-menu.aa-with-searches')
    assert suggestions.is_displayed()
    print('- Mobile search suggestions displayed')

    # 4898 - Update query suggestions so that they use Algolia indexes instead of JSON (EN only)
    resize.resizeDesktop(driver)
    header_search = driver.find_element(By.CSS_SELECTOR, 'div.cmp-header__search')
    search_field = header_search.find_element(By.CSS_SELECTOR, 'input#aa-search-input--header-desktop')
    search_field.send_keys("Energy")
    print('- "Energy" entered into search field')
    time.sleep(1)
    search_suggestions_dropdown = driver.find_element(By.CSS_SELECTOR, 'span.aa-dropdown-menu')
    assert "display: block;" in search_suggestions_dropdown.get_attribute('style')
    search_suggestion_terms = search_suggestions_dropdown.find_elements(By.CSS_SELECTOR, 'p')
    assert len(search_suggestion_terms) >= 3
    print('- 3 or more results found for "Energy", algolia terms in use')
