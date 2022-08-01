from selenium.webdriver.common.by import By
from importlib.machinery import SourceFileLoader
import requests

def runTest(baseUrl, driver, browser):

    print(' - Testing on {}'.format(browser))
    dismisscookie = SourceFileLoader('getcookiefile', '../Lib/dismisscookie.py').load_module()
    blogpostlist = SourceFileLoader('getblogpostlist', '../Lib/blog_post_list.py').load_module()
    resize = SourceFileLoader('getresize', '../Lib/resize.py').load_module()

    blogposts = blogpostlist.get_blog_posts()

    for post in blogposts:

        iterationUrl = "{baseUrl}{post}".format(baseUrl=baseUrl, post=post)
        resize.resizeDesktop(driver)
        driver.get(iterationUrl)
        dismisscookie.dismissCookieBanner(driver)
        print('\nVisiting: {iterationUrl}'.format(iterationUrl=iterationUrl))

        # ===== Breadcrumbs ===== #

        # Check if breadcrumb is found
        breadcrumbElem = driver.find_element(By.CSS_SELECTOR, '.breadcrumb')
        assert breadcrumbElem
        print('- Breadcrumb found')

        # Check the home link
        bcHomeLink = breadcrumbElem.find_element(By.CSS_SELECTOR, '.cmp-breadcrumb__list-item-link[title~="Home"] span')
        bcHomeLinkText = bcHomeLink.text
        assert bcHomeLinkText == "Home"
        print('- Breadcrumb home link found')

        # Home link URL
        bcHomeLinkUrl = breadcrumbElem.find_element(By.CSS_SELECTOR, '.cmp-breadcrumb__list-item-link[title~="Home"]').get_attribute('href')
        assert bcHomeLinkUrl == "{baseUrl}/en".format(baseUrl=baseUrl)
        print('- Home link correct "/en"')

        # Check the blog link
        bcBlogLink = breadcrumbElem.find_element(By.CSS_SELECTOR, '.cmp-breadcrumb__list-item-link[title="Blog home"] span')
        bcBlogLinkText = bcBlogLink.text
        assert bcBlogLinkText == "Blog home"
        print('- Breadcrumb blog link found')

        # Blog link URL
        bcBlogLinkUrl = breadcrumbElem.find_element(By.CSS_SELECTOR, '.cmp-breadcrumb__list-item-link[title="Blog home"]').get_attribute("href")
        assert bcBlogLinkUrl == "{baseUrl}/en/blog".format(baseUrl=baseUrl)
        print('- Blog link correct "/en/blog"')

        # ===== H1 ===== #

        blogTitle = driver.find_element(By.CSS_SELECTOR, 'h1.cmp-title__text')
        assert blogTitle
        print('- Blog post title found: "{blogTitle}"'.format(blogTitle=blogTitle.text))

        # ===== Hero image ===== #

        heroElem = driver.find_element(By.CSS_SELECTOR, '.hero-image')
        heroElemImage = heroElem.find_element(By.CSS_SELECTOR, '.cmp-hero-image')

        # Check if hero element found
        assert heroElem
        print('- Hero image container found')

        # Heros should at least be these sizes
        desktop = {
            "width" : 800,
            "height" : 350
        }
        mobile = {
            "width" : 350,
            "height" : 150
        }

        assert heroElemImage.size['height'] > desktop['height'] and heroElemImage.size['width'] > desktop['width']
        print('- Desktop Hero image size ok')
        
        # Check image resizes with screen
        resize.resizeMobile(driver)
        print('- Resized window to mobile')

        mobileHeroImage = driver.find_element(By.CSS_SELECTOR, '.cmp-hero-image')
        assert mobileHeroImage.size['height'] > mobile['height'] and mobileHeroImage.size['width'] > mobile['width']
        print('- Mobile hero image size ok')
        
        # ===== Dates ===== #

        dateElem = driver.find_element(By.CSS_SELECTOR, '.blog-dates')
        dateSections = dateElem.find_elements(By.CSS_SELECTOR, '.cmp-blog-dates__section')

        assert len(dateSections) == 2
        print('- Created and updated sections found')
        
        # Date titles - not all contain both a published and updated date
        postDateText = driver.find_elements(By.CSS_SELECTOR, '.cmp-blog-dates__section-text')
        for item in postDateText:
            text = item.text
            print('- Section title "{text}"'.format(text=text))
        
        postDateDates = driver.find_elements(By.CSS_SELECTOR, '.cmp-blog-dates__section-date')
        for item in postDateDates:
            text = item.text
            print('- Section date "{text}"'.format(text=text))

        postDateTextLen = len(postDateText)
        postDateDatesLen = len(postDateDates)

        # Warnings
        # If the updated date is present, but the title is not
        if postDateDatesLen == 2 and postDateTextLen < 2:
            message = "> WARNING: This post includes a last updated date but no 'Last updated' title\n    {iterationUrl}".format(
                iterationUrl=iterationUrl
            )
            print(message)
            
        # If the title is missing
        if postDateTextLen == 0:
            message = "> WARNING: This post is missing a published date\n    {iterationUrl}".format(
                iterationUrl=iterationUrl
            )
            print(message)

        # ===== Blog intro text ===== #

        blogIntroElem = driver.find_element(By.CSS_SELECTOR, '.cmp-text--blog-intro')
        assert blogIntroElem
        blogIntroText = blogIntroElem.text
        print("- Blog intro element found: '{blogIntroText}'".format(blogIntroText=blogIntroText))
        
        blogIntroStyles = {
            "border-top" : "8px solid rgb(111, 216, 216)",
            "border-bottom" : "8px solid rgb(111, 216, 216)",
            "margin" : "35px 0px 0px",
            "line-height" : "23px",
        }
        
        for key, value in blogIntroStyles.items():
            assert blogIntroElem.value_of_css_property(key) == value
            print('- Blog intro {key} correct: {value}'.format(key=key, value=value))
            
        # Confirm p tag margin
        blogIntroP = blogIntroElem.find_element(By.CSS_SELECTOR, 'p')
        blogIntroPMargin = blogIntroP.value_of_css_property('margin')
        
        assert blogIntroPMargin == "18px 0px"
        print('- Blog intro <p> margin ok')

        # ===== H2 ===== #

        blogH2Titles = driver.find_elements(By.CSS_SELECTOR, 'h2.cmp-title__text')
        blogH2count = len(blogH2Titles)
        # If there are no h2 elements
        if blogH2count >= 1:
            print('- {blogH2count} H2 title elements found'.format(blogH2count=blogH2count))
        else:
            message = "- WARNING: Blog post contains no H2 title elements\n    {iterationUrl}".format(
                iterationUrl=iterationUrl
            )
            print(message)

        # ===== Author Component ===== #
        
        blogAuthor = driver.find_element(By.CSS_SELECTOR, '.cmp-aboutauthor')

        assert blogAuthor

        print('- Blog author element found')
        blogAuthorName = blogAuthor.find_element(By.CSS_SELECTOR, '.cmp-aboutauthor__author')
        print('- Blog author name {blogAuthorName}'.format(blogAuthorName=blogAuthorName.text))

        # Confirm link exists and points to the right place
        blogAuthorLink = blogAuthor.find_element(By.CSS_SELECTOR, '.cmp-aboutauthor__link')
        blogAuthorLinkHref = blogAuthorLink.get_attribute('href')

        author_link_status = requests.get(blogAuthorLinkHref).status_code
        assert author_link_status == 200
        print('- Blog author link OK (200)')

        # Confirm correct font is used by the author component - 2976
        expectedFont = "Caveat, cursive"
        blogAuthorNameFont = blogAuthorName.value_of_css_property("font-family")
        assert blogAuthorNameFont == expectedFont
        print('- Author font correct: {expectedFont}'.format(expectedFont=expectedFont))

    # Blog Search Results / Blog list component
    # Test order of posts in blog results - Tickets 4141 and 5215
    
    blogListPage = "{}/en/blog/blog-list.html?qr=&page=1&sort=".format(baseUrl)
    driver.get(blogListPage)
    
    print('5215 - /blog-list page returns Error and not loading older blog posts')
    blogListItems = driver.find_elements(By.CSS_SELECTOR, 'a.cmp-blog-list__blog')
    assert len(blogListItems) > 0
    print('- Blog items found in blog list component')

    print('4141 - Checking that page 1 does not include posts from 2015')
    print(' - Visiting the blog list')
    blogDates = driver.find_elements(By.CSS_SELECTOR, 'span.cmp-blog-list__blog-date')
    assert len(blogDates) > 0
    print('- Blog dates found')
    for date in blogDates:
        dateText = date.text
        print(' - Blog date: {}'.format(dateText))

        if "2018" in dateText:
            message = "- Blog post on page 1 of results is dated 2018, possible ordering issue please check {}".format(blogListPage)
            print(message)
        elif "2018" not in dateText:
            print('- Blog post on page 1 of results not from 2018, ordering appears correct')
