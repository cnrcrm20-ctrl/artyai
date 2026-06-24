import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Her görev için en iyi ücretsiz model
MODELS = {
    "chat": "meta-llama/llama-3.3-70b-instruct:free",
    "code": "deepseek/deepseek-r1:free",
    "search": "google/gemini-2.0-flash-exp:free",
    "fast": "meta-llama/llama-3.1-8b-instruct:free",
    "creative": "mistralai/mistral-7b-instruct:free",
}

DEFAULT_MODEL = MODELS["chat"]
