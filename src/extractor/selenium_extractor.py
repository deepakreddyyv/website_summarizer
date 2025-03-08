from . import extractor_intferface as ei
from selenium import webdriver
from selenium.webdriver.common.by import By

class SeleniumFetcher(ei.DataFetcher):
    """
    Fetches data from a URL using Selenium for dynamic content rendering.
    """

    def __init__(self, url: str):
        """
        Initializes the SeleniumFetcher with a URL and starts a Chrome webdriver.

        Args:
            url (str): The URL to fetch.
        """
        self.url = url
        self.driver = webdriver.Chrome()
        self.title = None
        self.body = None
        self.soup = None
        self.links = []

    def fetch(self):
        """
        Fetches data from the URL using Selenium, extracts the title,
        and text from body and finds anchor tags.

        Returns:
            dict: A dictionary containing the title, body text, and anchor tags.
        """
        self.driver.get(self.url)  
        self.title = self.driver.title 
        self.body = self.driver.find_element(By.TAG_NAME, 'body').text
        self.links = [a.get_attribute('href') for a in self.driver.find_elements(By.TAG_NAME, 'a')]
        self.driver.quit()
