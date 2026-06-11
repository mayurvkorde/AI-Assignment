import os
from pathlib import Path
from typing import cast
from dotenv import load_dotenv

from pydantic_settings import BaseSettings

load_dotenv()

class Config(BaseSettings): # type: ignore [misc]
    """Represent Config data, """
    RDS_ASYNC_URI: str = cast("str", os.getenv("RDS_ASYNC_URI"))
    API_KEY: str = cast("str", os.getenv("API_KEY"))
    PORT: int = cast("int", os.getenv("PORT", 8000))
    AUTHORIZER_SECRET_KEY: str = cast("str", os.getenv("AUTHORIZER_SECRET_KEY"))
    OPENAI_API_KEY: str = cast("str", os.getenv("OPENAI_API_KEY"))

config = Config()