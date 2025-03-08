from google import genai
from google.genai import types

from llms.llms_interface import LLMSummarizer

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
