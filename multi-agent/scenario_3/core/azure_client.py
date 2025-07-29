# core/azure_client.py

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential


def connect_to_project(endpoint):
    """
    Establish connection to Azure AI Project using default credentials.

    Args:
        endpoint: Azure AI Project endpoint URL

    Returns:
        AIProjectClient: Connected Azure AI Project client

    Raises:
        Exception: If connection to Azure AI Project fails
    """
    print("🔗 Connecting to Azure AI Project...")

    try:
        client = AIProjectClient(
            endpoint=endpoint,
            credential=DefaultAzureCredential()
        )
        print(f"✅ Connected to Azure AI Project at: {endpoint}")
        return client

    except Exception as e:
        print(f"❌ Failed to connect to Azure AI Project at {endpoint}: {e}")
        print("💡 Please ensure you are authenticated with Azure CLI or have proper credentials configured")
        raise
