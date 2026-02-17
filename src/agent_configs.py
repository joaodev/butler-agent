import dotenv
import os
from openai import OpenAI


dotenv.load_dotenv()

api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL")

# Initialize the OpenAI client with values from environment variables.
# If no API key is available, keep the client as None and use a local fallback response.
client = OpenAI(api_key=api_key, base_url=base_url) if api_key else None

SYSTEM_PROMPT = """
You are a helpful assistant, your goal is to helper user.
You have an access to the wardrobe and weather.
Don't ask for permission to do the task, just do everything you can to help user.
"""

MODEL_NAME = "gpt-4o-mini"
MAX_ITERATIONS = 5

WARDROBE = {
    "blue weather": "dirty",
    "brown jacket": "dirty"
}

TOOLS_REGISTRY = [
    {
        "type": "function",
        "name": "check_weather",
        "description": "Check the current weather conditions.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "type": "function",
        "name": "get_wardrobe_items",
        "description": "Lists all clothing items in the wardrobe with their status (clean/dirty).",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "type": "function",
        "name": "wash_clothing",
        "description": "Wash a dirty clothing item to make it clean.",
        "parameters": {
            "type": "object",
            "properties": {
                "item_name": {
                    "type": "string",
                    "description": "Name of the clothing item to wash"
                }
            },
            "required": ["item_name"]
        }
    }
]