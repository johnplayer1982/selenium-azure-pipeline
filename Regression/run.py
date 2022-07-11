from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os, requests

# Components
import cookies
import breadcrumbs
import accordion_carousel
import article_feedback
import callouts
import chat
import emergency_banner
import footer_follow
import global_card
import header
import home_hero
import icon_anchor
import images
import local_navigation
import navigation
import overview_card
import section_hero
import seo

username = os.getenv("CBT_USERNAME")
authkey = os.getenv("CBT_AUTHKEY")

api_session = requests.Session()
api_session.auth = (username, authkey)
test_result = None
build = "1.8.4"
release = "Azure Staging Components - {}".format(build)
baseUrl = "https://test.moneyhelper.org.uk"

caps = {
    'name': '{}'.format(release),
    'build': '{}'.format(build),
    'platform': 'Windows',
    'browserName': 'Chrome',
    'screenResolution' : '1920x1080',
    'record_video' : 'true'
}

driver = webdriver.Remote(
    command_executor="http://%s:%s@hub.crossbrowsertesting.com/wd/hub"%(username, authkey),
    desired_capabilities=caps)

tests = {
    "Cookies" : cookies,
    "Breadcrumbs" : breadcrumbs,
    "Accordion Carousel" : accordion_carousel,
    "Article Feedback" : article_feedback,
    "Callouts" : callouts,
    "Chat" : chat,
    "Emergency Banner" : emergency_banner,
    "Footer Follow" : footer_follow,
    "Global Card" : global_card,
    "Header" : header,
    "Home Hero" : home_hero,
    "Icon Anchor" : icon_anchor,
    "Images" : images,
    "Local Navigation" : local_navigation,
    "Navigation" : navigation,
    "Overview Card" : overview_card,
    "Search" : search,
    "Section Hero" : section_hero,
    "SEO" : seo,
}

try:
    for key, value in tests.items():
        print('Testing {}'.format(key))
        value.runTest(baseUrl, driver)
        print('End of {} test\n'.format(key))
    test_result = 'pass'
except AssertionError as e:
    test_result = 'fail'
    raise

print("Done with session %s" % driver.session_id)
driver.quit()
# Here we make the api call to set the test's score.
# Pass it it passes, fail if an assertion fails, unset if the test didn't finish
if test_result is not None:
    api_session.put('https://crossbrowsertesting.com/api/v3/selenium/' + driver.session_id,
        data={'action':'set_score', 'score':test_result})

# Search
import search

api_session = requests.Session()
api_session.auth = (username, authkey)
test_result = None
release = "Azure Staging Search - {}".format(build)

caps = {
    'name': '{}'.format(release),
    'build': '{}'.format(build),
    'platform': 'Windows',
    'browserName': 'Edge',
    'screenResolution' : '1920x1080',
    'record_video' : 'true'
}

driver = webdriver.Remote(
    command_executor="http://%s:%s@hub.crossbrowsertesting.com/wd/hub"%(username, authkey),
    desired_capabilities=caps)

tests = {
    "Search" : search,
}

try:
    search.runTest(baseUrl, driver)
    test_result = 'pass'
except AssertionError as e:
    test_result = 'fail'
    raise

print("Done with session %s" % driver.session_id)
driver.quit()
# Here we make the api call to set the test's score.
# Pass it it passes, fail if an assertion fails, unset if the test didn't finish
if test_result is not None:
    api_session.put('https://crossbrowsertesting.com/api/v3/selenium/' + driver.session_id,
        data={'action':'set_score', 'score':test_result})

# Templates
import blog_post
import subcategory_page
import subcategory_article_list

api_session = requests.Session()
api_session.auth = (username, authkey)
test_result = None
release = "Azure Staging Templates - {}".format(build)

caps = {
    'name': '{}'.format(release),
    'build': '{}'.format(build),
    'platform': 'Windows',
    'browserName': 'Edge',
    'screenResolution' : '1920x1080',
    'record_video' : 'true'
}

driver = webdriver.Remote(
    command_executor="http://%s:%s@hub.crossbrowsertesting.com/wd/hub"%(username, authkey),
    desired_capabilities=caps)

tests = {
    "Blog Post" : blog_post,
    "Subcategory Page" : subcategory_page,
    "Subcategory Article List" : subcategory_article_list,
}

try:
    for key, value in tests.items():
        print('Testing {}'.format(key))
        value.runTest(baseUrl, driver)
        print('End of {} test\n'.format(key))
    test_result = 'pass'
except AssertionError as e:
    test_result = 'fail'
    raise

print("Done with session %s" % driver.session_id)
driver.quit()
# Here we make the api call to set the test's score.
# Pass it it passes, fail if an assertion fails, unset if the test didn't finish
if test_result is not None:
    api_session.put('https://crossbrowsertesting.com/api/v3/selenium/' + driver.session_id,
        data={'action':'set_score', 'score':test_result})
