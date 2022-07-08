from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from importlib.machinery import SourceFileLoader
import time

def runTest(baseUrl, driver):

    subcategorypages = SourceFileLoader('getsubcategorypages', '../Lib/subcategory_pages.py').load_module()

    urls = subcategorypages.get_subcategory_pages()

    for page in urls:

        iterationUrl = "{baseUrl}{page}".format(baseUrl=baseUrl, page=page)
        driver.get(iterationUrl)

        print("\nTesting {iterationUrl}".format(iterationUrl=iterationUrl))

        # Get the accordion buttons
        articleLists = driver.find_elements(By.CSS_SELECTOR, ".cmp-list-of-articles")

        for list in articleLists:

            # Try block as we want to allow the element to not be found in some short article lists
            try:
                viewAllBtn = list.find_element(By.CSS_SELECTOR, ".cmp-list-of-articles__accordion-heading")
                if viewAllBtn.is_displayed():

                    # Click the view all button
                    viewAllBtn.click()
                    print("- Button found and clicked")

                    # Check the accordion element displays
                    accordionElement = list.find_element(By.CSS_SELECTOR, ".cmp-list-of-articles__accordion")
                    assert accordionElement.get_attribute("data-topcontenaccordion") == "opened"
                    print("- Accordion element is open")

                    # Check the accordion content is visible
                    accordionContent = list.find_element(By.CSS_SELECTOR, ".cmp-list-of-articles__accordion-content")
                    time.sleep(0.2)
                    assert accordionContent.is_displayed()
                    print("- Accordion content visible")
                    
                    # Check the close button is visible
                    closeBtn = list.find_element(By.CSS_SELECTOR, ".cmp-list-of-articles__accordion-footer")
                    print("- Close button found")

                    # Click the close button
                    closeBtn.click()
                    print("- Clicked the close button")

                    assert accordionElement.get_attribute("data-topcontenaccordion") == "closed"
                    print("- Accordion element is closed\n")
                    
            except NoSuchElementException:
                print("- List isnt long enough to contain a view all button")
