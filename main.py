from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from utilities import Message, BrowserDriver, SelectorType, Selector
import os


def select_browser():
    browser: str = None
    while (browser != "F" and browser != "C"):
        browser = input("Select BROWSER(Navegador)\n"
                        "  F) Firefox\n"
                        "  C) Google Chrome\n"
                        "Option: ").upper()

        if browser != "F" and browser != "C":
            print(Message.ERROR.value
                  + f"'{browser}' is NOT a valid option for the BROWSER"
                  + Message.RESET.value)

    browser = (BrowserDriver.FIREFOX.name
               if (browser == 'F')
               else BrowserDriver.CHROME.name)

    print(Message.INFO.value
          + f"'{browser}' selected as browser"
          + Message.RESET.value)

    return browser


def start_browser(pathDriver: str, broswer: str):
    """Method that receives a path and the browser that
    will use Selenium [Firefox, Google Chrome, etc.] to initialize the browser

    Args:
        pathDriver (str): path where the driver is located\
        broswer (str): browser that uses selenium

    Returns:
        The initialized browser driver
        or "None" if the arguments were wrong
    """

    driver = None

    if broswer == BrowserDriver.FIREFOX.name:
        driver = webdriver.Firefox(
            executable_path=f"{pathDriver}/{BrowserDriver.FIREFOX.value}")
    elif broswer == BrowserDriver.CHROME.name:
        driver = webdriver.Firefox(
            executable_path=f"{pathDriver}/{BrowserDriver.CHROME.value}")

    return driver


def check_element_exists(selectorType: str, selector: str):
    """Checks if an element exists on the current website

    Args:
        selectorType (str): Selector type [css_selecetor, tag_name, name,
                            xpath, etc], for more information
                            see selenium documentation
        selector (str): Selector value

    Returns:
        bool: True if the selector exists,
              False if selector does not exist or selector type is wrong
    """

    try:
        if selectorType == SelectorType.TAG_NAME.value:
            driver.find_element_by_tag_name(selector)
        elif selectorType == SelectorType.CSS_SELECTOR.value:
            driver.find_element_by_css_selector(selector)
        else:
            return False
    except NoSuchElementException:
        return False
    return True


def select_user_twitter():
    username: str = input("Enter the username on Twitter: @").lower()
    url: str = f"https://twitter.com/{username}"
    print(f"Accessing: {url}")
    driver.get(url=url)

    if check_element_exists(SelectorType.TAG_NAME.value,
                            Selector.TWEET_TAG.value):
        print(Message.INFO.value
              + f"The user @{username} exists,"
              + "proceeding to download the text of the tweets")
    elif check_element_exists(SelectorType.CSS_SELECTOR.value,
                              Selector.PRIVATE_ACCOUNT_CSS.value):
        print(Message.WARNING.value
              + "The account is private"
              + Message.RESET.value)
    elif check_element_exists(SelectorType.CSS_SELECTOR.value,
                              Selector.PAGE_NOT_FOUND_CSS.value):
        print(Message.WARNING.value
              + "The account and/or user does not exist"
              + Message.RESET.value)
    else:
        print(Message.ERROR.value
              + "Selector type or selector value is wrong"
              + Message.RESET.value)


if __name__ == "__main__":
    browser: str = None
    driver = None

    browser = select_browser()
    pathDriver = os.path.abspath(path=BrowserDriver.PATH_DRIVERS.value)
    driver = start_browser(pathDriver=pathDriver, broswer=browser)
    driver.minimize_window()
    driver.implicitly_wait(10)  # *Delay time for browser actions

    select_user_twitter()
    driver.close()
