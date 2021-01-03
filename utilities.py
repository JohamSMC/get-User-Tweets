import enum

class Message(enum.Enum):
    ERROR    = "\033[1;31;40m" + "ERROR: "
    INFO     = "\033[1;32;40m" + "INFO: "
    WARNING  = "\033[1;33;40m" + "WARNING: "
    RESET    = "\033[0;37;49m \n"

class BrowserDriver(enum.Enum):
    PATH_DRIVERS = "browser-Drivers/"
    FIREFOX = "geckodriver"
    CHROME  = "chromedriver"
