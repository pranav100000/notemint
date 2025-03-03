import os
from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API settings
    API_V1_STR: str = "/api/v1"
    
    # CORS settings
    CORS_ORIGINS: List[str] = ["*"]
    
    # File storage settings
    MIDI_FILES_DIR: Path = Path("./midi_files")
    
    # Ensure the MIDI files directory exists
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        os.makedirs(self.MIDI_FILES_DIR, exist_ok=True)
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": True
    }


settings = Settings()