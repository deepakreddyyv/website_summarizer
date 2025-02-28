from google import genai
from google.genai import types

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

import requests
from abc import ABC, abstractmethod

from IPython.display import Markdown, display


class DataFetcher(ABC):
    """
    Abstract base class for fetching data from different sources.
    """

    @abstractmethod
    def fetch(self):
        """
        Abstract method to fetch data. Must be implemented by subclasses.
        """
        pass


class SoupFetcher(DataFetcher):
    """
    Fetches data from a URL using BeautifulSoup for parsing HTML.
    """

    def __init__(self, url=None, page_source=None):
        """
        Initializes the SoupFetcher with a URL or pre-parsed HTML.

        Args:
            url (str, optional): The URL to fetch. Defaults to None.
            page_source (BeautifulSoup, optional): Pre-parsed HTML. Defaults to None.
        """
        self.url = url
        self.title = None
        self.body = None
        self.soup = page_source

    def fetch(self):
        """
        Fetches data from the URL (or uses provided HTML), extracts the title,
        cleans the body text, and finds anchor tags.

        Returns:
            dict: A dictionary containing the title, cleaned body text, and anchor tags.
        """
        if self.soup is None:
            # Fetch data from URL if no page_source is provided
            data = requests.get(self.url)
            self.soup = BeautifulSoup(data.text, 'html.parser')
        # Extract the title, handle cases where title is not present.
        self.title = self.soup.title.string if self.soup.title else 'Title Not Found'
        # Remove irrelevant tags from the body like scripts, style, img, and input.
        for irrelvent in self.soup.body(['scripts', 'style', 'img', 'input']):
            irrelvent.decompose()
        # Get the cleaned text content of the body.
        self.body = self.soup.body.get_text()
        # Find all anchor tags in the document.
        self.anchor_tags = self.soup.find_all('a')
        return {'title': self.title, 'contents': self.body, 'anchor_tags': self.anchor_tags}


class SeleniumFetcher(DataFetcher):
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

    def fetch(self):
        """
        Fetches data from the URL using Selenium, extracts the title,
        and text from body and finds anchor tags.

        Returns:
            dict: A dictionary containing the title, body text, and anchor tags.
        """
        self.driver.get("https://openai.com/index/openai-o3-mini/")  # Navigates to the URL
        self.title = self.driver.title  # Gets the title from the page
        self.body = self.driver.find_element(By.TAG_NAME, 'body')  # Gets the body
        self.anchor_tags = self.driver.find_elements(By.TAG_NAME, 'a')  # Gets all anchor tags
        return {'title': self.title, 'contents': self.body.text, 'anchor_tags': self.anchor_tags}


class LLMSummarizer(ABC):
    """
    Abstract base class for LLM-based summarizers.
    """

    @abstractmethod
    def summarize(self):
        """
        Abstract method to summarize text. Must be implemented by subclasses.
        """
        pass


class GeminiSummarizer(LLMSummarizer):
    """
    Summarizes text using the Google Gemini model.
    """

    def __init__(self, user_prompt: str, system_prompt: str, **optional_params):
        """
        Initializes the GeminiSummarizer with prompts and optional parameters.

        Args:
            user_prompt (str): The prompt for the user.
            system_prompt (str): The system-level instructions for the LLM.
            **optional_params: Additional parameters for the Gemini API.
        """
        self.client = genai.Client()  # store the google api key in environment variable
        self.user_prompt = user_prompt
        self.system_prompt = system_prompt
        self.optional_params = optional_params

    def summarize(self):
        """
        Generates a summary using the Gemini model.

        Returns:
            google.ai.generativelanguage_v1beta.types.generate_content_response.GenerateContentResponse: The response from the Gemini API.
        """
        response = self.client.models.generate_content(
            model='gemini-2.0-flash',
            contents=self.user_prompt,
            config=types.GenerateContentConfig(
                **self.optional_params
            )
        )
        return response


def main():
    """
    Main function to fetch website data, summarize it using Gemini, and save the summary.
    """
    url = "https://openai.com/index/openai-o3-mini/"
    # Using SeleniumFetcher to handle potential dynamic content
    fetcher = SeleniumFetcher(url)
    data = fetcher.fetch()

    system_prompt = "you are a very talented Text summarizer,\
    summarize the given text in simple english highlite the important events in bullet points and pls translate to english whenever required\
    "
    user_prompt = f"Your are looking at the website article titled {data['title']},\
    pls summarize the follow up article if there are additional ifo like events or updates pls \
    summarize these too and return in markdown\n\n\n\n{data['contents']}"

    # Initializing GeminiSummarizer with specific parameters
    gemini_llm = GeminiSummarizer(user_prompt, system_prompt, seed=42, max_output_tokens=1000, temperature=0.5)
    summary = gemini_llm.summarize()

    # Save the summary to a markdown file.
    with open('../outputs/summary.md', 'w') as f:
        f.write(summary.text)


# Execute the main function when the script is run.
main()
