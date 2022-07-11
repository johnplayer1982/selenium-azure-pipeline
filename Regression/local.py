from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os, requests

import cookies
import breadcrumbs
import accordion_carousel
import article_feedback
import blog_post
import callouts
import chat
import emergency_banner
import footer_follow
import global_card
import header
import home_hero
import icon_anchor
import images
import subcategory_article_list
import subcategory_page
import local_navigation
import navigation
import overview_card
import search
import section_hero
import seo
import seperator_anchor
import social_sharing
import tag_selector
import teasers
import text
import misc

from selenium.webdriver.chrome.options import Options

baseUrl = "https://test.moneyhelper.org.uk"

# driver = webdriver.Safari()
CHROME_VERSION_PC = os.getenv('CHROME_VERSION_PC')
DRIVER_BIN = "..\chromedriver_104.exe"
options = Options()
options.binary_location = r"C:\Program Files\Google\Chrome Beta\Application\chrome.exe"
driver = webdriver.Chrome(chrome_options=options, executable_path=DRIVER_BIN)

tests = {
    "Cookies" : cookies,
    "Breadcrumbs" : breadcrumbs,
    "Accordion Carousel" : accordion_carousel,
    "Article Feedback" : article_feedback,
    "Blog Post" : blog_post,
    "Callouts" : callouts,
    "Chat" : chat,
    "Emergency Banner" : emergency_banner,
    "Footer Follow" : footer_follow,
    "Global Card" : global_card,
    "Header" : header,
    "Home Hero" : home_hero,
    "Icon Anchor" : icon_anchor,
    "Images" : images,
    "Subcategory Article List" : subcategory_article_list,
    "Subcategory Page" : subcategory_page,
    "Local Navigation" : local_navigation,
    "Navigation" : navigation,
    "Overview Card" : overview_card,
    "Search" : search,
    "Section Hero" : section_hero,
    "SEO" : seo,
    "Seperator Anchor" : seperator_anchor,
    "Social Sharing" : social_sharing,
    "Tag Selector" : tag_selector,
    "Teasers" : teasers,
    "Text" : text,
    "Misc Tests" : misc,
}

for key, value in tests.items():
    print('> Testing {}\n'.format(key))
    value.runTest(baseUrl, driver)
    print('\n> End of {} test\n'.format(key))

driver.quit()
