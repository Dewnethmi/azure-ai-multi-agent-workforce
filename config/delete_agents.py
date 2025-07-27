import os
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

load_dotenv()


def setup_project_client():
    """Initialize and return the Azure AI Project client."""
    PROJECT_ENDPOINT = os.getenv("PROJECT_ENDPOINT")
    MODEL_DEPLOYMENT_NAME = os.getenv("MODEL_DEPLOYMENT_NAME")
    if not PROJECT_ENDPOINT:
        raise ValueError("PROJECT_ENDPOINT is not set in the .env file.")
    if not MODEL_DEPLOYMENT_NAME:
        raise ValueError("MODEL_DEPLOYMENT_NAME is not set in the .env file.")
    try:
        project_client = AIProjectClient(
            endpoint=PROJECT_ENDPOINT,
            credential=DefaultAzureCredential(),
        )
    except Exception as e:
        print(f"❌ Error initializing AIProjectClient: {e}")
        raise
    return project_client


def delete_single_agent(agent_id: str):
    """Delete a single agent by its ID, after checking its existence."""
    print("✨ Delete Single Agent")
    client = setup_project_client()
    existing = [agent.id for agent in client.agents.list_agents(limit=100)]
    if agent_id not in existing:
        print(f"🤖 Agent ID {agent_id} not found. No deletion performed.")
        return

    print(f"🔄 Starting deletion of agent ID: {agent_id}")
    try:
        client.agents.delete_agent(agent_id)
        print(f"✅ Deleted agent ID: {agent_id}")
    except Exception as e:
        print(f"❌ Failed to delete agent ID {agent_id}: {e}")


def delete_multiple_agents(agent_ids: list[str]):
    """Delete multiple agents by their IDs, skipping non-existent ones."""
    print("✨ Delete Multiple Agents")
    client = setup_project_client()
    existing = [agent.id for agent in client.agents.list_agents(limit=100)]

    to_delete = [aid for aid in agent_ids if aid in existing]
    missing = [aid for aid in agent_ids if aid not in existing]

    if not to_delete:
        print("🤖 None of the specified agent IDs were found. No deletions.")
        return

    if missing:
        print(f"⚠️ Some IDs not found and will be skipped: {missing}")

    for aid in to_delete:
        print(f"🔄 Starting deletion of agent ID: {aid}")
        try:
            client.agents.delete_agent(aid)
            print(f"✅ Deleted agent ID: {aid}")
        except Exception as e:
            print(f"❌ Failed to delete agent ID {aid}: {e}")


def delete_all_agents():
    """Delete all agents in the project."""
    print("✨ Delete All Agents")
    client = setup_project_client()
    all_ids = [agent.id for agent in client.agents.list_agents(limit=100)]
    if not all_ids:
        print("🤖 No agents found to delete.")
        return

    print(f"🔁 Found {len(all_ids)} agents. Proceeding to delete...")
    for aid in all_ids:
        print(f"🔄 Starting deletion of agent ID: {aid}")
        try:
            client.agents.delete_agent(aid)
            print(f"✅ Deleted agent ID: {aid}")
        except Exception as e:
            print(f"❌ Failed to delete agent ID {aid}: {e}")


if __name__ == "__main__":
    # Delete a single agent
    # delete_single_agent("asst_eZ8H7qwf88i9Z5Gho5werdkW")

    # Delete multiple agents
    # delete_multiple_agents([
    #     "asst_gLxnQAEyUyeYAqqgovMLxUGO",
    #     "asst_OZRHTkR4hqS0iee0ErHyhb88",
    #     "asst_TndAxHg6mgEJ3rEelItzIKKq"
    # ])

    # Delete all agents
    delete_all_agents()
