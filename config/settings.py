from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    groq_api_key: str = os.getenv("GROQ_API_KEY")
    model_name: str = "llama-3.1-8b-instant"
    max_tokens: int = 4_000
    system_prompt: str = "Actúa como pirata"

settings = Settings()
