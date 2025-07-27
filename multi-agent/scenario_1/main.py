import time
import sys
import logging
import os
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import (
    ConnectedAgentTool,
    MessageRole,
    ListSortOrder
)

# ──────────────────────────────────────────────
# 🔧 Logging Setup
# ──────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout)],
    format='📄 [%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s]\n👉🏽 %(message)s'
)

# ──────────────────────────────────────────────
# 🔽 Load Configuration
# ──────────────────────────────────────────────


def load_configuration():
    logging.info("🔄 Loading environment variables...")
    load_dotenv()

    env = os.getenv("ENVIRONMENT", "development")
    endpoint = os.getenv("PROJECT_ENDPOINT")
    model_name = os.getenv("MODEL_DEPLOYMENT_NAME")

    logging.info(f"🌐 ENVIRONMENT: {env}")

    if not endpoint:
        raise ValueError("❌ PROJECT_ENDPOINT is not set.")
    if not model_name:
        raise ValueError("❌ MODEL_DEPLOYMENT_NAME is not set.")

    logging.info("✅ Configuration loaded.")

    return endpoint, model_name

# ──────────────────────────────────────────────
# 🔗 Connect to Azure AI Project
# ──────────────────────────────────────────────


def connect_to_project(endpoint):
    logging.info("🔗 Connecting to Azure AI Project...")

    try:
        client = AIProjectClient(
            endpoint=endpoint,
            credential=DefaultAzureCredential()
        )
        logging.info(f"✅ Connected to Azure AI Project at: {endpoint}")
        return client

    except Exception as e:
        logging.error(
            f"❌ Failed to connect to Azure AI Project at {endpoint}: {e}")
        raise  # Optionally re-raise if you want the program to halt


# ──────────────────────────────────────────────
# 🤖 Create Connected Agent
# ──────────────────────────────────────────────


def create_inventory_agent(project, model_name):
    agent_name: str = "inventory_agent"
    agent_description: str = "Provides inventory details"
    agent_instructions: str = (
        "You are responsible for providing the latest inventory data. "
        "Here is the current list of items in stock:\n"
        "- 🍎 Apples: 150 units\n"
        "- 🍞 Bread: 80 units\n"
        "- 🧼 Soap: 45 units\n"
        "- 🥛 Milk: 100 units\n"
        "When asked about inventory, respond with the most accurate information available."
    )

    logging.info(f"🤖 Creating connected agent ({agent_name})...")

    try:
        agent = project.agents.create_agent(
            model=model_name,
            name=agent_name,
            description=agent_description,
            instructions=agent_instructions,
        )

        logging.info(f"✅ {agent_name} created: {agent.id}")

        logging.info(f"⚙️ Connecting agent to the tools ({agent_name})...")

        connected_tool = ConnectedAgentTool(
            id=agent.id,
            name=agent_name,
            description="Responds with current inventory levels"
        )

        logging.info(f"✅ {agent_name} connected to tools.")

        return agent, connected_tool

    except Exception as e:
        logging.error(
            f"❌ Failed to create inventory agent ({agent_name}): {e}")
        raise  # Re-raise to signal failure upstream


# ──────────────────────────────────────────────
# 🧠 Create Main Agent and Connect Tool
# ──────────────────────────────────────────────


def create_main_agent(project, model_name, connected_tool):
    agent_name: str = "store_manager_agent"
    agent_description: str = "Manages inventory-related queries"
    agent_instructions: str = (
        "You are the store manager. If a user asks about available stock or inventory, "
        "use the connected tool to respond with up-to-date inventory information."
    )

    logging.info(f"🤖 Creating main agent ({agent_name})...")

    try:
        agent = project.agents.create_agent(
            model=model_name,
            name=agent_name,
            description=agent_description,
            instructions=agent_instructions,
            tools=connected_tool.definitions,
        )

        logging.info(f"✅ {agent_name} created: {agent.id}")
        return agent

    except Exception as e:
        logging.error(f"❌ Failed to create main agent ({agent_name}): {e}")
        raise


# ──────────────────────────────────────────────
# 🧵 Create Conversation Thread
# ──────────────────────────────────────────────


def create_thread(project):
    logging.info("🧵 Creating conversation thread...")

    try:
        thread = project.agents.threads.create()
        logging.info(f"✅ Thread created: {thread.id}")
        return thread

    except Exception as e:
        logging.error(f"❌ Failed to create conversation thread: {e}")
        raise


# ──────────────────────────────────────────────
# 💬 Send User Message
# ──────────────────────────────────────────────


def send_user_message(project, thread, content):
    logging.info(f"💬 User message: {content}")
    logging.info("📨 Sending user message to agent...")

    try:
        message = project.agents.messages.create(
            thread_id=thread.id,
            role=MessageRole.USER,
            content=content
        )
        logging.info(f"✅ Message sent: {message.id}")
        return message

    except Exception as e:
        logging.error(f"❌ Failed to send user message: {e}")
        raise


# ──────────────────────────────────────────────
# 🏃 Run Agent
# ──────────────────────────────────────────────


def run_agent(project, thread, agent, poll_interval=2, timeout=60):
    logging.info("🏃 Starting agent run...")

    try:
        run = project.agents.runs.create(
            thread_id=thread.id,
            agent_id=agent.id
        )
        logging.info(f"🔄 Run initiated: {run.id} — Status: {run.status}")

        # Poll for completion
        start_time = time.time()
        while run.status in ["queued", "in_progress"]:
            if time.time() - start_time > timeout:
                raise TimeoutError(
                    "⏰ Run timed out while waiting for completion.")

            time.sleep(poll_interval)
            run = project.agents.runs.get(thread_id=thread.id, run_id=run.id)
            logging.info(f"📡 Run status: {run.status}")

        # Final status
        if run.status == "failed":
            logging.error(f"❌ Run failed: {run.last_error}")
        else:
            logging.info(f"✅ Run completed with status: {run.status}")

        return run

    except Exception as e:
        logging.error(f"💥 Failed to run agent: {e}", exc_info=True)
        raise


# ──────────────────────────────────────────────
# 📥 Fetch and Display Messages
# ──────────────────────────────────────────────


def display_agent_responses(project, thread, run):
    logging.info("📥 Fetching messages from thread...")

    try:
        messages = project.agents.messages.list(
            thread_id=thread.id,
            order=ListSortOrder.ASCENDING
        )

        for msg in messages:
            if msg.run_id == run.id and msg.text_messages:
                try:
                    last_message = msg.text_messages[-1].text.value
                    logging.info(
                        f"\n🧠 {msg.role.capitalize()}: {last_message}")
                except (IndexError, AttributeError) as inner_e:
                    logging.warning(
                        f"⚠️ Skipped a malformed message: {inner_e}")

    except Exception as e:
        logging.error(f"❌ Failed to fetch/display agent responses: {e}")
        raise


# ──────────────────────────────────────────────
# 🗑️ Optional Cleanup
# ──────────────────────────────────────────────


def delete_agents(project, *agents):
    for agent in agents:
        try:
            logging.info(f"🗑️ Deleting agent: {agent.name}")
            project.agents.delete_agent(agent.id)
            logging.info(f"✅ Deleted agent: {agent.name}")
        except Exception as e:
            logging.error(f"❌ Failed to delete agent {agent.name}: {e}")

    logging.info("✅ Agent cleanup process completed.")


# ──────────────────────────────────────────────
# 🚀 Main Execution
# ──────────────────────────────────────────────


def main():
    try:
        logging.info("🚀 Starting main execution...")

        endpoint, model_name = load_configuration()
        project = connect_to_project(endpoint)

        _, connected_tool = create_inventory_agent(project, model_name)
        main_agent = create_main_agent(project, model_name, connected_tool)

        thread = create_thread(project)

        user_message = "Do you have any apples in stock?"
        send_user_message(project, thread, user_message)

        run = run_agent(project, thread, main_agent)
        display_agent_responses(project, thread, run)

        # Uncomment to delete agents after execution
        # delete_agents(project, main_agent, inventory_agent)

        logging.info("🎉 Program completed successfully.")

    except KeyboardInterrupt:
        logging.info("🛑 Program shutdown via Ctrl+C")
    except Exception as e:
        logging.error(f"💥 Unexpected error in main(): {e}", exc_info=True)
    finally:
        logging.info("🔴 Program terminated")


if __name__ == "__main__":
    main()
