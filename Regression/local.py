from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os, requests
import cookies, breadcrumbs, accordion_carousel, article_feedback, blog_post, callouts, chat

baseUrl = "https://test.moneyhelper.org.uk"

driver = webdriver.Safari()

tests = {
    "Cookies" : cookies,
    "Breadcrumbs" : breadcrumbs,
    "Accordion Carousel" : accordion_carousel,
    "Article Feedback" : article_feedback,
    "Blog Post" : blog_post,
    "Callouts" : callouts,
    "Chat" : chat,
}

for key, value in tests.items():
    print('> Testing {}\n'.format(key))
    value.runTest(baseUrl, driver)
    print('\n> End of {} test\n'.format(key))
