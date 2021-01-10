import enum


class Message(enum.Enum):
    ERROR = "\033[1;31;40m" + "ERROR: "
    INFO = "\033[1;32;40m" + "INFO: "
    WARNING = "\033[1;33;40m" + "WARNING: "
    RESET = "\033[0;37;49m \n"


class BrowserDriver(enum.Enum):
    PATH_DRIVERS = "browser-Drivers/"
    FIREFOX = "geckodriver"
    CHROME = "chromedriver"


class SelectorType(enum.Enum):
    TAG_NAME = "TAG_NAME"
    CSS_SELECTOR = "CSS_SELECTOR"


class Selector(enum.Enum):
    PRIVATE_ACCOUNT_CSS = (
        "span.r-1b6yd1w > svg:nth-child(1)> g:nth-child(1)"
        + "> path:nth-child(1)")
    PAGE_NOT_FOUND_CSS = "h1.css-901oao > span:nth-child(1)"
    TWEET_TAG = "article"
    RETWEET = ""
