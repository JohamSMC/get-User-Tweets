from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from utilities import Message, BrowserDriver, SelectorType, Selector
import os
import csv


def select_browser():
    browser: str = None
    while (browser != "F" and browser != "C"):
        browser = input(Message.REQUEST.value
                        + "Select the BROWSER:\n"
                        + "\t    F) Firefox\n"
                        + "\t    C) Google Chrome\n"
                        + "\t Option: "
                        + Message.INPUT.value).upper()
        print(Message.RESET.value, end="")
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
            driver = webdriver.Chrome(
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
        elif selectorType == SelectorType.XPATH.value:
            driver.find_element_by_xpath(selector)
        else:
            return False
    except NoSuchElementException:
        return False
    return True


def select_twitter_user():
    username: str = input(Message.REQUEST.value
                          + "Type the username: "
                          + Message.INPUT.value + "@")
    print(Message.RESET.value, end="")
    url: str = f"https://twitter.com/{username}"
    print(Message.INFO.value
          + f"Accessing: {url}"
          + Message.RESET.value)
    driver.get(url=url)

    # ? Check if the account Exists
    if check_element_exists(SelectorType.TAG_NAME.value,
                            Selector.TWEET_TAG.value):
        print(Message.INFO.value
              + f"The user with username: @{username} if it exists"
              + Message.RESET.value)
    # ? Check if the account is Private
    elif check_element_exists(SelectorType.CSS_SELECTOR.value,
                              Selector.PRIVATE_ACCOUNT_CSS.value):
        print(Message.WARNING.value
              + "The account is private"
              + Message.RESET.value)
        username = None
    # ? Check if the account is suspended
    elif check_element_exists(SelectorType.XPATH.value,
                              Selector.SUSPENDED_ACCOUNT_XPATH.value):
        print(Message.WARNING.value
              + "The account is suspended"
                + Message.RESET.value)
        username = None
    # ? Check if the account does NOT Exist
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


def get_tweets(username: str, limitTweets: int):
    number_tweets_obtained: int = 0
    while check_element_exists(SelectorType.TAG_NAME.value, Selector.TWEET_TAG.value):
        if limitTweets > 0 and limitTweets == number_tweets_obtained:
            break
        fullTweet = driver.find_element_by_tag_name(Selector.TWEET_TAG.value)

        isRetweeted = is_retweet(fullTweet=fullTweet)
        textTweet = get_tweet_text(fullTweet=fullTweet, isRetweeted=isRetweeted)
        dateTweet = get_tweet_date(fullTweet=fullTweet)

        yield({"username": username,
               "date_tweet": dateTweet,
               "is_retweeted": isRetweeted,
               "text_tweet": textTweet})

        number_tweets_obtained += 1
        remove_tweet()


def select_tweet_number_limit(username: str):
    limitTweets: int = -1
    while (limitTweets < 0):
        limitTweets = input(Message.REQUEST.value
                            + "Type the number of tweets you want to get from the user:"
                            + f" @{username}, or type '0' to get all the tweets: "
                            + Message.INPUT.value)
        print(Message.RESET.value, end="")
        if not limitTweets.isnumeric():
            print(Message.WARNING.value
                  + "The value must be numerical and greater than or equal to 0"
                  + Message.RESET.value)
            limitTweets = -1
        else:
            limitTweets = int(limitTweets)
    else:
        return limitTweets


def build_csv_tweets(tweets: iter, username: str, fileNumber: str = "1"):
    CSV_COLUMNS = ["username", "date_tweet", "is_retweeted", "text_tweet"]
    if len(fileNumber) == 1:
        fileNumber = "0" + fileNumber
    CSV_NAME = f"tweets/tweets-{username}_{fileNumber}.csv"
    with open(file=CSV_NAME, mode='w',) as csv_file:
        writer = csv.DictWriter(f=csv_file, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        tweet_counter: int = 0
        for index, tweet in enumerate(tweets, start=1):
            writer.writerow(tweet)
            tweet_counter += 1
            print(f"N of tweets downloaded till now {index}")
        return tweet_counter


if __name__ == "__main__":
    browser: str = None
    driver = None
    username: str = None
    limitTweets = None

    try:
        browser = select_browser()
        pathDriver = os.path.abspath(path=BrowserDriver.PATH_DRIVERS.value)
        driver = start_browser(pathDriver=pathDriver, broswer=browser)
        if driver is not None:
            tweets = []
            driver.minimize_window()
            driver.implicitly_wait(12)  # *Delay time for browser actions
            username = select_twitter_user()
            if username is not None:
                limitTweets = select_tweet_number_limit(username=username)
                tweets = get_tweets(username=username, limitTweets=limitTweets)
                if tweets is not None:
                    tweet_counter = build_csv_tweets(tweets=tweets, username=username)
                    print(Message.INFO.value
                          + f"The total N of TWEETS: {tweet_counter} from USERNAME: @{username}"
                          + "\nCheck in the folder 'tweets' the csv file(s) with the tweets")
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
    except KeyboardInterrupt:
        print("\n" + Message.WARNING.value
              + "The script was interrupted by the keyboard command 'Crtl + C'."
              + Message.RESET.value)
    except Exception as e:
        print("\n" + Message.ERROR.value
              + "Unexpected Error \nERROR INFORMATION: " + str(e)
              + Message.RESET.value)
