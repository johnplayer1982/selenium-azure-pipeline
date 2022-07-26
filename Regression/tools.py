from selenium.webdriver.common.by import By
from importlib.machinery import SourceFileLoader
import time, requests

def verify_status_code(tool_url):
    # Status code
    status_code = requests.get(tool_url).status_code
    if status_code == 200:
        print(' - Tool landing page reachable, status code 200')
    else:
        raise AssertionError(" - Tool landing page not reachable")

def runTest(baseUrl, driver):
    
    resize = SourceFileLoader('getresize', '../Lib/resize.py').load_module()
    dismisscookie = SourceFileLoader('getcookiefile', '../Lib/dismisscookie.py').load_module()

    locales = {
        "/en",
        "/cy"
    }

    tools = {
        "Universal Credit" : "/benefits/universal-credit/money-manager",
        "Money Navigtor" : "/money-troubles/coronavirus/money-navigator-tool",
        "Budget Planner" : "/everyday-money/budgeting/budget-planner",
        "Car Cost Calculator" : "/everyday-money/buying-and-running-a-car/car-costs-calculator",
        "Payment Accounts Comparison" : "/everyday-money/banking/compare-bank-account-fees-and-charges",
        "Credit Card Calculator" : "/everyday-money/credit-and-purchases/credit-card-calculator",
        "Loan Calculator" : "/everyday-money/credit-and-purchases/loan-calculator",
        "Travel Insurance Directory" : "/everyday-money/insurance/travel-insurance-directory",
        "Baby Cost Calculator" : "/family-and-care/becoming-a-parent/baby-costs-calculator",
        "Baby Money Timeline" : "/family-and-care/becoming-a-parent/baby-money-timeline",
        "LBTT Scotland" : "/homes/buying-a-home/land-and-buildings-transaction-tax-calculator-scotland",
        "LTT Wales" : "/homes/buying-a-home/land-transaction-tax-calculator-wales",
        "Mortgage Calculator" : "/homes/buying-a-home/mortgage-calculator",
        "Mortgage Affordability Calculator" : "/homes/buying-a-home/mortgage-affordability-calculator",
        "Stamp Duty Calculator" : "/homes/buying-a-home/stamp-duty-calculator",
        "Debt Advice Locator" : "/money-troubles/dealing-with-debt/debt-advice-locator",
        "Retirement Adviser Directory" : "/pensions-and-retirement/taking-your-pension/find-a-retirement-adviser",
        "Find Your Pension Type" : "/pensions-and-retirement/pension-wise/find-out-your-pension-type",
        "Pension Calculator" : "/pensions-and-retirement/pensions-basics/pension-calculator",
        "Workplace Pensions Contribution Calculator" : "/pensions-and-retirement/auto-enrolment/workplace-pension-calculator",
        "Savings Calculator" : "/savings/how-to-save/savings-calculator",
        "Redundancy Pay Calculator" : "/work/losing-your-job/redundancy-pay-calculator"
    }

    comparison_tools = {
        "Compare Annuities EN" : "https://comparison.moneyhelper.org.uk/en/guaranteed-income-for-life/your-details",
        "Compare Annuities CY" : "https://comparison.moneyhelper.org.uk/cy/guaranteed-income-for-life/your-details",
        "Pension Drawdown EN" : "https://comparison.moneyhelper.org.uk/en/tools/drawdown-investment-pathways/get-started",
        "Pension Drawdown CY" : "https://comparison.moneyhelper.org.uk/cy/tools/drawdown-investment-pathways/get-started"
    }

    # Dismiss cookie banner for this session
    driver.get(baseUrl)
    time.sleep(1)
    dismisscookie.dismissCookieBanner(driver)
    resize.resizeDesktop(driver)

    for item in locales:

        for key, value in tools.items():

            print('\nVisiting {}'.format(key))
            tool_url = "{baseUrl}{item}{tool}".format(baseUrl=baseUrl, item=item, tool=value)

            verify_status_code(tool_url)
            print(tool_url)
            driver.get(tool_url)
            time.sleep(1)

            # Find the button
            start_tool_btn = driver.find_element(By.CSS_SELECTOR, 'a.cmp-button__primary')
            if start_tool_btn:
                print(' - Primary button found')
                start_tool_btn.click()
                print(' - Primary button clicked')
            else:
                raise AssertionError(" - Primary button not found on {}".format(key))

    print('\n> All iframed tools reachable')

    for key, value in comparison_tools.items():

        print('\n Checking {} is reachable'.format(key))
        verify_status_code(value)
        driver.get(value)

    print('\n> All comparison tools reachable')  
