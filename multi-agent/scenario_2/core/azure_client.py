import logging
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential


def connect_to_project(endpoint):
    """Establish connection to Azure AI Project."""
    # logging.info("🔗 Connecting to Azure AI Project...")
    print("🔗 Connecting to Azure AI Project...")

    try:
        client = AIProjectClient(
            endpoint=endpoint,
            credential=DefaultAzureCredential()
        )
        # logging.info(f"✅ Connected to Azure AI Project at: {endpoint}")
        print(f"✅ Connected to Azure AI Project at: {endpoint}")
        return client

    except Exception as e:
        # logging.error(
        #     f"❌ Failed to connect to Azure AI Project at {endpoint}: {e}")
        print(f"❌ Failed to connect to Azure AI Project at {endpoint}: {e}")
        raise
