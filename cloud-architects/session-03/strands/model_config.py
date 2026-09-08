import os
from dotenv import load_dotenv
from strands.models.openai import OpenAIModel


load_dotenv()

def get_model():
    required = ["OPENAI_API_KEY", "OPENAI_BASE_URL", "OPENAI_MODEL"]
    missing = [name for name in required if not os.getenv(name)]
    if missing:
        raise RuntimeError(
            "Missing environment variables: " + ", ".join(missing) +
            ". Copy .env.example to .env and fill in your values."
        )

    return OpenAIModel(
        client_args = {
            "api_key": os.getenv("OPENAI_API_KEY"),
            "base_url": os.getenv("OPENAI_BASE_URL"),
        },
        model_id = os.getenv("OPENAI_MODEL"),
        params = {
            "temperature": 0.7,
            "max_tokens": 1500,
        }
    )