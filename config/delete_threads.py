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
        return AIProjectClient(
            endpoint=PROJECT_ENDPOINT,
            credential=DefaultAzureCredential(),
        )
    except Exception as e:
        print(f"❌ Error initializing AIProjectClient: {e}")
        raise


def delete_single_thread(thread_id: str):
    """Delete a single thread by its ID, after verifying existence."""
    print("✨ Delete Single Thread")
    client = setup_project_client()
    existing = [t.id for t in client.agents.threads.list(limit=100)]
    if thread_id not in existing:
        print(f"🧵 Thread ID {thread_id} not found. No deletion performed.")
        return

    print(f"🔄 Starting deletion of thread ID: {thread_id}")
    try:
        client.agents.threads.delete(thread_id=thread_id)
        print(f"✅ Deleted thread ID: {thread_id}")
    except Exception as e:
        print(f"❌ Failed to delete thread ID {thread_id}: {e}")


def delete_multiple_threads(thread_ids: list[str]):
    """Delete multiple threads by their IDs, skipping non-existent ones."""
    print("✨ Delete Multiple Threads")
    client = setup_project_client()
    existing = [t.id for t in client.agents.threads.list(limit=100)]

    to_delete = [tid for tid in thread_ids if tid in existing]
    missing = [tid for tid in thread_ids if tid not in existing]

    if not to_delete:
        print("🧵 None of the specified thread IDs were found. No deletions.")
        return

    if missing:
        print(f"⚠️ Some IDs not found and skipped: {missing}")

    for tid in to_delete:
        print(f"🔄 Starting deletion of thread ID: {tid}")
        try:
            client.agents.threads.delete(thread_id=tid)
            print(f"✅ Deleted thread ID: {tid}")
        except Exception as e:
            print(f"❌ Failed to delete thread ID {tid}: {e}")


def delete_all_threads():
    """Delete all threads in the project."""
    print("✨ Delete All Threads")
    client = setup_project_client()
    all_ids = [t.id for t in client.agents.threads.list(limit=100)]
    if not all_ids:
        print("🧵 No threads found to delete.")
        return

    print(f"🔁 Found {len(all_ids)} threads. Proceeding to delete...")
    for tid in all_ids:
        print(f"🔄 Starting deletion of thread ID: {tid}")
        try:
            client.agents.threads.delete(thread_id=tid)
            print(f"✅ Deleted thread ID: {tid}")
        except Exception as e:
            print(f"❌ Failed to delete thread ID {tid}: {e}")


if __name__ == "__main__":
    # Delete a single thread
    # delete_single_thread("thread_HscuXrOA04AZYt3JLnzvMdKG")

    # Delete multiple threads
    # delete_multiple_threads([
    #     "thread_76Q0ygGLWGoYnX1LL31usiw5",
    #     "thread_HBlcTcB4WpkOhTdDBzQt5Ud9",
    #     "thread_OUxhLIRJWLioSJPTiar83wgP"
    # ])

    # Delete all threads
    delete_all_threads()
