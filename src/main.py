import streamlit as st
from google import genai
from google.genai import types
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from abc import ABC, abstractmethod
from IPython.display import Markdown, display  # Import only if needed for display


class DataFetcher(ABC):
    """Abstract base class for fetching data from different sources."""

    @abstractmethod
    def fetch(self):
        """Abstract method to fetch data. Must be implemented by subclasses."""
        pass


class SoupFetcher(DataFetcher):
    """Fetches data from a URL using BeautifulSoup for parsing HTML."""

    def __init__(self, url=None, page_source=None):
        """Initializes the SoupFetcher with a URL or pre-parsed HTML."""
        self.url = url
        self.title = None
        self.body = None
        self.soup = page_source

    def fetch(self):
        """Fetches data, extracts title, cleans body, and finds anchor tags."""
        if self.soup is None:
            try:
                data = requests.get(self.url, timeout=10)
                data.raise_for_status()  # Raise HTTPError for bad responses
                self.soup = BeautifulSoup(data.text, 'html.parser')
            except requests.exceptions.RequestException as e:
                st.error(f"Error fetching URL: {e}")
                return None

        if self.soup is None:
            return None

        self.title = self.soup.title.string if self.soup.title else 'Title Not Found'
        for irrelevant in self.soup.body(['script', 'style', 'img', 'input']):
            irrelevant.decompose()
        self.body = self.soup.body.get_text()
        self.anchor_tags = self.soup.find_all('a')
        return {'title': self.title, 'contents': self.body, 'anchor_tags': self.anchor_tags}


class SeleniumFetcher(DataFetcher):
    """Fetches data from a URL using Selenium for dynamic content rendering."""

    def __init__(self, url: str):
        """Initializes the SeleniumFetcher with a URL and starts a Chrome webdriver."""
        self.url = url
        self.driver = None  # Initialize driver to None
        self.title = None
        self.body = None
        self.soup = None

    def fetch(self):
        """Fetches data from the URL using Selenium, extracts the title and text."""
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("headless")  # Run Chrome in headless mode
            self.driver = webdriver.Chrome(options=options)
            self.driver.get(self.url)  # Navigates to the URL
            self.title = self.driver.title  # Gets the title from the page
            body_element = self.driver.find_element(By.TAG_NAME, 'body')  # Gets the body element
            self.body = body_element.text  # Gets the text from the body element
            self.anchor_tags = self.driver.find_elements(By.TAG_NAME, 'a')  # Gets all anchor tags
            return {'title': self.title, 'contents': self.body, 'anchor_tags': self.anchor_tags}
        except Exception as e:
            st.error(f"Error fetching with Selenium: {e}")
            return None
        finally:
            if self.driver:
                self.driver.quit()  # Ensure driver is closed


class LLMSummarizer(ABC):
    """Abstract base class for LLM-based summarizers."""

    @abstractmethod
    def summarize(self):
        """Abstract method to summarize text. Must be implemented by subclasses."""
        pass


class GeminiSummarizer(LLMSummarizer):
    """Summarizes text using the Google Gemini model."""

    def __init__(self, user_prompt: str, **optional_params):
        """Initializes the GeminiSummarizer with prompts and optional parameters."""
        self.client = genai.Client()
        self.user_prompt = user_prompt
        self.optional_params = optional_params

    def summarize(self):
        """Generates a summary using the Gemini model."""
        try:
            response = self.client.models.generate_content(
                model='gemini-2.0-flash',
                contents=self.user_prompt,
                config=types.GenerateContentConfig(**self.optional_params)
            )

            return response
        except Exception as e:
            st.error(f"Error during summarization: {e}")
            return None

# --- Streamlit App ---
st.set_page_config(page_title="Web Summarizer", page_icon=":newspaper:")
st.title("Web Article Summarizer :newspaper:")
st.markdown("Enter a URL to summarize the article using Google Gemini.")

url = st.text_input("Enter URL:", placeholder="https://example.com")
fetcher_type = st.selectbox("Choose Fetcher:", ["Selenium(Recommended)", "BeautifulSoup"])

if url:
    with st.spinner(f"Fetching with {fetcher_type} and Summarizing..."):
        fetcher = SeleniumFetcher(url)
        if fetcher_type == "BeautifulSoup":
            fetcher = SoupFetcher(url=url)

        data = fetcher.fetch()

        if data:
            system_prompt = ("You are a talented text summarizer. Summarize the given text in simple "
                             "English, highlight important events in bullet points and create seperate sections, "
                             "and translate to English whenever required.")
            user_prompt = (f"You are looking at the website article titled {data['title']}." 
                           "Please summarize the following "
                           f"article. If there are additional infos like events or updates, please "
                           f"summarize these too:\n\n\n\n{data['contents']}")

            gemini_llm = GeminiSummarizer(user_prompt, system_instruction=system_prompt, seed=42, max_output_tokens=1000, temperature=0.5)
            summary = gemini_llm.summarize()

            if summary and summary.text:
                st.subheader("Summary:")
                st.markdown(summary.text)
            else:
                st.error("Failed to generate a summary.")
        else:
            st.error("Failed to fetch data from the URL.")