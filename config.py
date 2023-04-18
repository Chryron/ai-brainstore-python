import os
import abc
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

class Singleton(abc.ABCMeta, type):
    """
    Singleton metaclass for ensuring only one instance of a class.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Call method for the singleton metaclass."""
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(
                *args, **kwargs)
        return cls._instances[cls]

class Config(metaclass=Singleton):
    """
    Configuration class to store the state of bools for different scripts access.
    """

    def __init__(self):
        """Initialize the Config class"""

        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.endpoint = os.getenv("ENDPOINT")
        self.vectorizer = os.getenv("VECTORIZER")
        self.fast_llm_model = "gpt-3.5-turbo"