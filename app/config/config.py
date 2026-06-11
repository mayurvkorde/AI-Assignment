import os
from pathlib import Path
from typing import cast
from dotenv import load_dotenv

from pydantic_settings import BaseSettings

load_dotenv()

class Config(BaseSettings): # type: ignore [misc]
    """Represent Config data, """
    pass

config = Config()