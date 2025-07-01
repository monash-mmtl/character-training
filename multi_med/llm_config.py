import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieving API keys from environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
OPEN_ROUTER_KEY = os.getenv('OPEN_ROUTER_KEY')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')

# Model configurations dictionary
MODEL_CONFIGS = {
    "gpt-4o": {
        "config_list": [{
            "model": "gpt-4o",
            "api_key": OPENAI_API_KEY,
            "base_url": "https://api.openai.com/v1",
        }],
        "temperature": 0.1,
    },
    "gpt-4o-mini": {
        "config_list": [{
            "model": "gpt-4o-mini",
            "api_key": OPENAI_API_KEY,
            "base_url": "https://api.openai.com/v1",
        }],
        "temperature": 0.1,
    },
    "gemini-2.0-flash": {
        "config_list": [{
            "model": "gemini-2.0-flash",
            "api_key": GEMINI_API_KEY,
            "api_type": "google",
        }],
        "temperature": 0.1,
    },
        "gemini-2.5-flash": {
        "config_list": [{
            "model": "gemini-2.5-flash",
            "api_key": GEMINI_API_KEY,
            "api_type": "google",
        }],
        "temperature": 0.1,
    },
    "deepseek-V3": {
        "config_list": [{
            "model": "deepseek-chat",
            "base_url": "https://api.deepseek.com/v1",
            "api_type": "deepseek",
            "api_key": DEEPSEEK_API_KEY,
        }],
        "temperature": 0.1,
    },
}

def get_model_config(model_name):
    """
    Get the configuration for a specific model.
    
    Args:
        model_name (str): Name of the model to get configuration for
        
    Returns:
        dict: Configuration for the specified model
    """
    if model_name not in MODEL_CONFIGS:
        raise ValueError(f"Model {model_name} not found in configurations")
    return MODEL_CONFIGS[model_name] 