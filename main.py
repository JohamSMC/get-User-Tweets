from selenium import webdriver
from utilities import Message, BrowserDriver
import os


def select_browser() :
    browser:str = None
    while (browser != "F" and browser != "C"):
        browser = input("Select BROWSER(Navegador)\n"
                    "  F) Firefox\n"
                    "  C) Google Chrome\n"
                    "Option: ").upper()

        if browser != "F" and browser != "C":
            print(Message.ERROR.value
                + f"'{browser}' is NOT a valid option for the BROWSER"
                + Message.RESET.value)

    browser = BrowserDriver.FIREFOX.name if (browser == 'F') else BrowserDriver.CHROME.name

    print(Message.INFO.value
    + f"'{browser}' selected as browser"
    + Message.RESET.value)

    return browser


def start_browser(pathDriver : str, broswer : str):
    """
    Method that receives a path and the browser that
    will use Selenium [Firefox, Google Chrome, etc.] to initialize the browser

    Args:
        pathDriver (str): [path where the driver is located]
        broswer (str): [browser that uses selenium]

    Returns:
        The initialized browser driver
        or "None" if the arguments were wrong
    """

    driver = None

    if broswer == BrowserDriver.FIREFOX.name :
        driver = webdriver.Firefox(executable_path=f"{pathDriver}/{BrowserDriver.FIREFOX.value}")
    elif broswer == BrowserDriver.CHROME.name :
        driver = webdriver.Firefox(executable_path=f"{pathDriver}/{BrowserDriver.CHROME.value}")

    return driver


if __name__ == "__main__":
    browser:str = None
    driver = None

    browser  = select_browser()
    pathDriver = os.path.abspath(path=BrowserDriver.PATH_DRIVERS.value)
    driver = start_browser(pathDriver=pathDriver, broswer=browser)
    driver.minimize_window()
