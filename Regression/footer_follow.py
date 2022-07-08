from selenium.webdriver.common.by import By
from importlib.machinery import SourceFileLoader

def runTest(baseUrl, driver):

    resize = SourceFileLoader('getresize', '../Lib/resize.py').load_module()

    # Maximise window
    resize.resizeDesktop(driver)
    print("- Maximising window")

    locales = [
        {
            "lang": "/en",
            "facebook": "https://www.facebook.com/MoneyHelperUK", 
            "twitter" : "https://twitter.com/MoneyHelperUK", 
            "youtube" : "https://www.youtube.com/channel/UCDwjX78G1j_m2zWvPhZSTcw"
        },
        {
            "lang": "/cy", 
            "facebook": "https://www.facebook.com/HelpwrArian", 
            "twitter" : "https://twitter.com/HelpwrArian", 
            "youtube" : "https://www.youtube.com/channel/UCDwjX78G1j_m2zWvPhZSTcw"
        }
    ]

    for locale in locales:

        language = locale["lang"]
        facebookUrl = locale["facebook"]
        twitterUrl = locale["twitter"]
        youtubeUrl = locale["youtube"]

        iterationUrl = "{baseUrl}{lang}".format(baseUrl=baseUrl, lang=language)
        driver.get(iterationUrl)
        print("\nVisiting {iterationUrl}".format(iterationUrl=iterationUrl))

        facebookBtn = driver.find_element(By.CSS_SELECTOR, ".cmp-footer__social--link-facebook")
        twitterBtn = driver.find_element(By.CSS_SELECTOR, ".cmp-footer__social--link-twitter")
        youtubeBtn = driver.find_element(By.CSS_SELECTOR, ".cmp-footer__social--link-youtube")

        assert facebookBtn.get_attribute("href") == facebookUrl
        print("- Facebook link correct for {language}: {facebookUrl}".format(language=language, facebookUrl=facebookUrl))
        
        assert twitterBtn.get_attribute("href") == twitterUrl
        print("- Twitter link correct for {language}: {twitterUrl}".format(language=language, twitterUrl=twitterUrl))
        
        assert youtubeBtn.get_attribute("href") == youtubeUrl
        print("- Youtube link correct for {language}: {youtubeUrl}".format(language=language, youtubeUrl=youtubeUrl))
