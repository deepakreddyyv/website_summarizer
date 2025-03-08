from abc import ABC, abstractmethod

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