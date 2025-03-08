from abc import ABC, abstractmethod

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