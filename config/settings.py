import sys
import logging
import os
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# ──────────────────────────────────────────────
# 🔧 Logging Setup
# ──────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout)],
    format='📄 [%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s]\n👉🏽 %(message)s'
)

# ──────────────────────────────────────────────
# ✅ Load and Validate Configuration
# ──────────────────────────────────────────────


def load_configuration():
    logging.info("🔄 Loading environment variables...")
    load_dotenv()

    env = os.getenv("ENVIRONMENT", "development")
    debug_mode = os.getenv("DEBUG_MODE", "false").lower() == "true"
    timeout = os.getenv("REQUEST_TIMEOUT", "30")
    endpoint = os.getenv("PROJECT_ENDPOINT")
    model_name = os.getenv("MODEL_DEPLOYMENT_NAME")
    agent_id = os.getenv("AGENT_ID")
    thread_id = os.getenv("THREAD_ID")

    missing = []
    if not endpoint:
        missing.append("PROJECT_ENDPOINT")
    if not model_name:
        missing.append("MODEL_DEPLOYMENT_NAME")
    if not agent_id:
        missing.append("AGENT_ID")
    if not thread_id:
        missing.append("THREAD_ID")

    if missing:
        for var in missing:
            logging.error(f"❌ Missing required environment variable: {var}")
        raise EnvironmentError("❌ Environment misconfiguration detected.")

    logging.info("✅ Configuration loaded successfully.")
    return env, debug_mode, timeout, endpoint, model_name, agent_id, thread_id

# ──────────────────────────────────────────────
# 🔗 Test Azure AI Project Connection
# ──────────────────────────────────────────────


def test_project_connection(endpoint):
    logging.info("🔗 Connecting to Azure AI Project...")

    try:
        client = AIProjectClient(
            endpoint=endpoint,
            credential=DefaultAzureCredential()
        )
        logging.info(
            f"✅ Successfully connected to Azure AI Project at: {endpoint}")
        return client
    except Exception as e:
        logging.error(f"❌ Failed to connect to Azure AI Project: {e}")
        raise


# ──────────────────────────────────────────────
# 🚀 Main Execution
# ──────────────────────────────────────────────
if __name__ == "__main__":
    try:
        env, debug_mode, timeout, endpoint, model_name, agent_id, thread_id = load_configuration()
        client = test_project_connection(endpoint)

        logging.info(f"🌐 ENVIRONMENT: {env}")
        logging.info(f"🐞 DEBUG_MODE: {debug_mode}")
        logging.info(f"⏰ REQUEST_TIMEOUT: {timeout} seconds")

        logging.info(f"🔗 PROJECT_ENDPOINT: {endpoint}")
        logging.info(f"🧠 MODEL_DEPLOYMENT_NAME: {model_name}")
        logging.info(f"🆔 AGENT_ID: {agent_id}")
        logging.info(f"🧵 THREAD_ID: {thread_id}")
        logging.info(f"🤖 CLIENT INSTANCE: {client}")

        logging.info(
            "🎉 Configuration and connection test completed successfully.")

    except Exception as e:
        logging.error(
            f"💥 Fatal error during initialization: {e}", exc_info=True)
