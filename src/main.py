from google import genai
from google.genai import types

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

import requests
from abc import ABC, abstractmethod

from IPython.display import Markdown, display

class DataFetcher(ABC):

    @abstractmethod
    def fetch(self):
        pass

class SoupFetcher(DataFetcher):

    def __init__(self, url=None, page_source=None):
        self.url = url
        self.title = None
        self.body = None
        self.soup = page_source
    
    def fetch(self):
        if self.soup is None:
            data = requests.get(self.url)
            self.soup = BeautifulSoup(data.text, 'html.parser')
        self.title = self.soup.title.string if self.soup.title else 'Title Not Found'
        for irrelvent in self.soup.body(['scripts', 'style', 'img', 'input']):
            irrelvent.decompose()
        self.body = self.soup.body.get_text()
        self.anchor_tags = self.soup.find_all('a')
        return {'title': self.title, 'contents': self.body, 'anchor_tags': self.anchor_tags}

class SeleniumFetcher(DataFetcher):
    
    def __init__(self, url:str):
        self.url = url
        self.driver = webdriver.Chrome()
        self.title = None
        self.body = None
        self.soup = None
    
    def fetch(self):
        self.driver.get("https://openai.com/index/openai-o3-mini/")
        self.title = self.driver.title
        self.body = self.driver.find_element(By.TAG_NAME, 'body')
        self.anchor_tags = self.driver.find_elements(By.TAG_NAME, 'a')
        return {'title': self.title, 'contents': self.body.text, 'anchor_tags': self.anchor_tags}
    
class LLMSummarizer(ABC):

    @abstractmethod
    def summarize(self):
        pass


class GeminiSummarizer(LLMSummarizer):

    def __init__(self, user_prompt:str, system_prompt:str, **optional_params):
        self.client = genai.Client() # store the google api key in environment variable
        self.user_prompt = user_prompt
        self.system_prompt = system_prompt
        self.optional_params = optional_params

    def summarize(self):
        response = self.client.models.generate_content(
            model='gemini-2.0-flash',
            contents=self.user_prompt,
            config=types.GenerateContentConfig(
                **self.optional_params
            )
        )
        return response
    

    
def main():
    url = "https://openai.com/index/openai-o3-mini/"
    fetcher = SeleniumFetcher(url)
    data = fetcher.fetch()
    
    system_prompt = "you are a very talented Text summarizer,\
    summarize the given text in simple english highlite the important events in bullet points and pls translate to english whenever required\
    "
    user_prompt = f"Your are looking at the website article titled {data['title']},\
    pls summarize the follow up article if there are additional ifo like events or updates pls \
    summarize these too and return in markdown\n\n\n\n{data['contents']}"

    gemini_llm = GeminiSummarizer(user_prompt, system_prompt, seed=42, max_output_tokens=1000, temperature=0.5)
    summary = gemini_llm.summarize()

    with open('../outputs/summary.md', 'w') as f:
        f.write(summary.text)

main()
    


