# settings.py

import os
from dotenv import load_dotenv


def load_configuration():
    """
    Load and validate environment configuration for Azure AI Foundry.

    Returns:
        tuple: (endpoint, model_name) - Azure project endpoint and model deployment name

    Raises:
        ValueError: If required environment variables are not set
    """
    try:
        print("🔄 Loading environment variables...")
        load_dotenv()

        env = os.getenv("ENVIRONMENT", "development")
        endpoint = os.getenv("PROJECT_ENDPOINT")
        model = os.getenv("MODEL_DEPLOYMENT_NAME")

        print(f"🌐 ENVIRONMENT: {env}")

        if not endpoint or not model:
            raise ValueError(
                "❌ PROJECT_ENDPOINT or MODEL_DEPLOYMENT_NAME not set in environment variables.")

        print("✅ Configuration loaded successfully.")
        return endpoint, model

    except Exception as e:
        print(f"❌ Failed to load configuration: {e}")
        raise
