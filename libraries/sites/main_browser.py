"""Base Site module."""
from RPA.Browser.Selenium import Selenium
from selenium.webdriver.chrome.options import Options


class Sites:
    """Base class for all sites."""

    def __init__(self, url):
        """Functions initialise the class."""
        self.browser = Selenium()
        self.url = url

    def setup_browser(self):
        """Setup the browser."""
        options = Options()
        options.add_argument("--disable-logging")
        # options.add_argument("--headless")
        self.browser.open_available_browser(options=options, maximized=True)
