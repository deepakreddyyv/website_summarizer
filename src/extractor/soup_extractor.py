from extractor.extractor_intferface import DataFetcher
import requests
from bs4 import BeautifulSoup

class SoupFetcher(DataFetcher):
    """
    Fetches data from a URL using BeautifulSoup for parsing HTML.
    """

    def __init__(self, url=None):
        """
        Initializes the SoupFetcher with a URL or pre-parsed HTML.

        Args:
            url (str, optional): The URL to fetch. Defaults to None.
            page_source (BeautifulSoup, optional): Pre-parsed HTML. Defaults to None.
        """
        self.url = url
        self.title = None
        self.body = None
        self.soup = None
        self.links = []

    def fetch(self):
        """
        Fetches data from the URL (or uses provided HTML), extracts the title,
        cleans the body text, and finds anchor tags.

        Returns:
            dict: A dictionary containing the title, cleaned body text, and anchor tags.
        """
        if self.soup is None:
            data = requests.get(self.url)
            self.soup = BeautifulSoup(data.text, 'html.parser')
        if self.soup is None or self.soup.body is None:
            return None
        self.title = self.soup.title.string if self.soup.title else 'Title Not Found'
        for irrelvent in self.soup.body(['scripts', 'style', 'img', 'input']):
            irrelvent.decompose()
        self.body = self.soup.body.get_text()
        for tag in self.soup.find_all('a'):
            if tag.get('href') is not None and tag.get('href').startswith('http'):
                self.links.append(tag.get('href'))
            elif tag.get('href') is not None and tag.get('href').startswith('/'):
                self.links.append(self.url + tag.get('href'))
