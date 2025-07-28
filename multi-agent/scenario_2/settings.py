import os
import logging
from dotenv import load_dotenv


def setup_logging():
    """Configure logging for the fitness advisor application."""
    logging.basicConfig(
        level=logging.INFO,
        handlers=[logging.StreamHandler()],
        format='🏋️ [%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s]\n👉 %(message)s'
    )


def load_configuration():
    """Load and validate environment configuration."""
    # logging.info("🔄 Loading environment variables...")
    print("🔄 Loading environment variables...")
    load_dotenv()

    env = os.getenv("ENVIRONMENT", "development")
    endpoint = os.getenv("PROJECT_ENDPOINT")
    model_name = os.getenv("MODEL_DEPLOYMENT_NAME")

    # logging.info(f"🌐 ENVIRONMENT: {env}")
    print(f"🌐 ENVIRONMENT: {env}")

    if not endpoint:
        raise ValueError("❌ PROJECT_ENDPOINT is not set.")
    if not model_name:
        raise ValueError("❌ MODEL_DEPLOYMENT_NAME is not set.")

    # logging.info("✅ Configuration loaded successfully.")
    print("✅ Configuration loaded successfully.")
    return endpoint, model_name
