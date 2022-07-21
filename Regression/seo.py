from selenium.webdriver.common.by import By
from importlib.machinery import SourceFileLoader
import time

def runTest(baseUrl, driver):
    
    eachpagetype = SourceFileLoader('geteachpagetype', '../Lib/each_page_type.py').load_module()
    dismisscookie = SourceFileLoader('getcookiefile', '../Lib/dismisscookie.py').load_module()

    urls = {
        "EN Home" : "/en", # EN home
        "CY Home" : "/cy", # CY home
        "Blog Post" : "/en/blog/scams-and-fraud/how-to-spot-and-avoid-dating-scams", # Blog post
        "Article Page" : "/en/pensions-and-retirement/building-your-retirement-pot", # Article
        "Tools Template" : "/en/homes/buying-a-home/mortgage-calculator", # Tools template
        "L1 Landing Page" : "/en/money-troubles", # L1
        "L2 Landing Page" : "/en/money-troubles/dealing-with-debt", #L2
        "Search Results Page" : "/en/search-results.html?q=benefits", # Search Results
    }

    tags = {
        "Canonical" : 'link[rel="canonical"]',
        "Body" : "body",
        "HTML" : "html",
        "Head" : "head",
        "Title" : "title",
        "Meta description" : 'meta[name="description"]',
        "Meta description" : 'meta[name="viewport"]'
    }

    siteUrl = "{}/en".format(baseUrl)
    driver.get(siteUrl)
    dismisscookie.dismissCookieBanner(driver)

    for key, value in urls.items():
        print('\n- Checking template {}'.format(key))
        iteration_url = "{baseUrl}{value}".format(baseUrl=baseUrl, value=value)
        driver.get(iteration_url)

        # HTML Lang attribute present
        html_tag = driver.find_element(By.CSS_SELECTOR, 'html')
        if "/en" in iteration_url:
            assert html_tag.get_attribute('lang') == "en"
        elif "/cy" in iteration_url:
            assert html_tag.get_attribute('lang') == "cy"
        else:
            raise AssertionError("html tag does not contain correct lang attribute")
        print(' + Correct lang attribute found on html tag')

        # H1 text aligns with title tag content
        if "Home" not in key:
            h1_text = driver.find_element(By.CSS_SELECTOR, 'h1').text
            page_title = driver.find_element(By.CSS_SELECTOR, 'title').get_attribute('innerText')
            
            # Convert to lowercase
            page_title = page_title.lower()
            h1_text = h1_text.lower()
            # Replace amps with and for alternative expected text
            h1_text_formatted = h1_text.replace("&", "and")

            if "search results for" in h1_text_formatted:
                h1_text_formatted = h1_text_formatted.replace("for", "")

            assert h1_text in page_title or h1_text_formatted in page_title or h1_text_formatted in page_title or page_title in h1_text_formatted
            print(' + Page title contains the page H1')

        for key, value in tags.items():
            target_tag = driver.find_elements(By.CSS_SELECTOR, value)
            assert target_tag
            assert len(target_tag) == 1
            print(" + Only 1 {} tag found".format(key))

    for key, value in urls.items():

        og_tags = {
            "og:title",
            "og:url",
            "og:type",
            "og:site_name",
            "og:image",
            "og:image:width",
            "og:image:height",
        }

        iteration_url = "{baseUrl}{value}".format(baseUrl=baseUrl, value=value)
        driver.get(iteration_url)
        print(' - Visiting {}'.format(iteration_url))
        for og in og_tags:
            print(og)
            og_tags = driver.find_elements(By.CSS_SELECTOR, 'meta[property="{}"]'.format(og))
            og_tags_count = len(og_tags)
            print('   + {} found'.format(og_tags_count))
            assert og_tags_count == 1

    if "test.moneyhelper" in baseUrl:
        print('4512 - Remove indexing from staging/test environments')
        data = eachpagetype.get_each_page_type()
        expected_tag = 'meta[content="noindex"]'
        for item in data:
            url = "{baseUrl}{item}".format(baseUrl=baseUrl, item=item)
            print(" + Checking {}".format(url))
            driver.get(url)
            assert driver.find_element(By.CSS_SELECTOR, expected_tag)
            print('  - noindex found')
