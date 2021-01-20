from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from utilities import Message, BrowserDriver, SelectorType, Selector
import os
import csv


def select_browser():
    browser: str = None
    while (browser != "F" and browser != "C"):
        browser = input("Select BROWSER(Navegador)\n"
                        "  F) Firefox\n"
                        "  C) Google Chrome\n"
                        "Option: ").upper()

        if browser != "F" and browser != "C":
            print(Message.WARNING.value
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
        or the browser cannot be initialized
    """

    driver = None

    try:
        if broswer == BrowserDriver.FIREFOX.name:
            driver = webdriver.Firefox(
                executable_path=f"{pathDriver}/{BrowserDriver.FIREFOX.value}")
        elif broswer == BrowserDriver.CHROME.name:
            driver = webdriver.Firefox(
                executable_path=f"{pathDriver}/{BrowserDriver.CHROME.value}")
    finally:
        return driver


def check_element_exists(selectorType: str, selector: str):
    """Checks if an element exists on the current website

    Args:
        selectorType (str): Selector type [css_selecetor, tag_name, name, xpath, etc],
                            for more information see selenium documentation
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


def select_twitter_user():
    username: str = input("Enter the username on Twitter: @")
    url: str = f"https://twitter.com/{username}"
    print(f"Accessing: {url}")
    driver.get(url=url)

    if check_element_exists(SelectorType.TAG_NAME.value,
                            Selector.TWEET_TAG.value):
        print(Message.INFO.value
              + f"The user @{username} exists,"
              + "proceeding to download the text of the tweets"
              + Message.RESET.value)
    elif check_element_exists(SelectorType.CSS_SELECTOR.value,
                              Selector.PRIVATE_ACCOUNT_CSS.value):
        print(Message.WARNING.value
              + "The account is private"
              + Message.RESET.value)
        username = None
    elif check_element_exists(SelectorType.CSS_SELECTOR.value,
                              Selector.PAGE_NOT_FOUND_CSS.value):
        print(Message.WARNING.value
              + "The account and/or user does not exist"
              + Message.RESET.value)
        username = None
    else:
        print(Message.ERROR.value
              + "Selector type or selector value is wrong"
              + Message.RESET.value)
        username = None

    return username


def is_retweet(fullTweet: WebElement):
    """[summary]

    Args:
        fullTweet (WebElement): WebElement which has all the content of the tweet
    Returns:
        bool: True if Tweet is a Retweet or False if Not a Retweet
    """
    if fullTweet.text.split("\n")[0] != fullTweet.text.split("\n")[1][1:]:
        return True
    else:
        return False


def get_tweet_text(fullTweet: WebElement, isRetweeted: bool):
    if isRetweeted:
        textTweet = fullTweet.text.split("\n")[5:]
    else:
        textTweet = fullTweet.text.split("\n")[4:]

    while(textTweet[-1].isdigit()):
        textTweet.pop()

    return "".join(textTweet)


def get_tweet_date(fullTweet: WebElement):
    return str(fullTweet.find_element_by_tag_name("time").get_attribute("datetime"))


def remove_tweet():
    """
    Remove the first tweet that appears in the browser
    """
    driver.execute_script("return document.getElementsByTagName('article')[0].remove();")


def get_tweets(username: str):
    while check_element_exists(SelectorType.TAG_NAME.value, Selector.TWEET_TAG.value):
        fullTweet = driver.find_element_by_tag_name(Selector.TWEET_TAG.value)

        isRetweeted = is_retweet(fullTweet=fullTweet)
        textTweet = get_tweet_text(fullTweet=fullTweet, isRetweeted=isRetweeted)
        dateTweet = get_tweet_date(fullTweet=fullTweet)

        yield({"username": username,
               "date_tweet": dateTweet,
               "is_retweeted": isRetweeted,
               "text_tweet": textTweet})

        remove_tweet()


if __name__ == "__main__":
    browser: str = None
    driver = None
    username: str = None

    browser = select_browser()
    pathDriver = os.path.abspath(path=BrowserDriver.PATH_DRIVERS.value)
    driver = start_browser(pathDriver=pathDriver, broswer=browser)
    if driver is not None:
        tweets = []
        driver.minimize_window()
        driver.implicitly_wait(15)  # *Delay time for browser actions
        username = select_twitter_user()
        tweets = get_tweets(username=username)
        if tweets is not None:
            for tweet in tweets:
                print(tweet, end="\n")
        else:
            print(Message.WARNING.value
                  + f"The user: {username} has no tweets in his account"
                  + Message.RESET.value)

        driver.close()

    else:
        print(Message.ERROR.value
              + "The browser could not be initialized, check that the version of the driver "
              + "matches the version of the browser you have installed, "
              + "and that the driver is in the browser-Drivers folder"
              + Message.RESET.value)
