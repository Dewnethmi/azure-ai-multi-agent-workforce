import os
import time
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import FunctionTool, ToolSet, ListSortOrder
from tools import get_company_details


# ---------------------------------------------
# Project setup functions
# ---------------------------------------------

print("🔄 Loading environment variables...")
load_dotenv()


def setup_project_client():
    """Initialize the AIProjectClient with required credentials and environment variables."""

    PROJECT_ENDPOINT = os.getenv("PROJECT_ENDPOINT")
    MODEL_DEPLOYMENT_NAME = os.getenv("MODEL_DEPLOYMENT_NAME")

    if not PROJECT_ENDPOINT:
        raise ValueError("❌ PROJECT_ENDPOINT is not set in the .env file.")
    if not MODEL_DEPLOYMENT_NAME:
        raise ValueError(
            "❌ MODEL_DEPLOYMENT_NAME is not set in the .env file.")

    print("🔗 Connecting to Azure AI Project...")

    try:
        project_client = AIProjectClient(
            endpoint=PROJECT_ENDPOINT,
            credential=DefaultAzureCredential(),
        )
        print("✅ Azure AI Project Connected!")
    except Exception as e:
        print(f"❌ Error initializing AIProjectClient: {e}")
        raise

    return project_client, MODEL_DEPLOYMENT_NAME


def setup_toolset():
    """Define and return toolset containing user-defined functions."""

    print("🛠️ Setting up agent tool configuration...")

    user_functions = {get_company_details}
    functions = FunctionTool(user_functions)
    toolset = ToolSet()
    toolset.add(functions)
    print(f"✅ User toolset defined: {toolset}")
    return toolset

# ---------------------------------------------
# Creation of new agent & thread
# ---------------------------------------------


def create_agent(project_client, model_deployment_name):
    """Create a new AI agent with toolset attached."""

    print("🤖 Creating a new agent...")

    try:
        agent_name: str = "company-info-agent-001"

        agent_description: str = (
            "A smart company information assistant designed to provide users with all relevant "
            "details about the company, including contact info, address, website, mission, vision, "
            "values, privacy policy, and terms and conditions."
        )

        agent_instructions: str = (
            "You are an expert assistant that provides company information. Answer user queries "
            "about the company's details, mission, vision, values, contact info, and legal policies. "
            "Always provide accurate, clear, and professional responses."
        )

        agent_toolset = setup_toolset()

        project_client.agents.enable_auto_function_calls(agent_toolset)

        agent = project_client.agents.create_agent(
            model=model_deployment_name,
            name=agent_name,
            instructions=agent_instructions,
            description=agent_description,
            toolset=agent_toolset,
        )
        print(f"✅ Agent created! ID: {agent.id}")
    except Exception as e:
        print(f"❌ Error creating agent: {e}")
        raise

    return agent


def create_thread(project_client):
    """Create a new conversation thread."""

    print("🧵 Creating a new conversation thread...")
    try:
        thread = project_client.agents.threads.create()
        print(f"✅ Thread created! ID: {thread.id}")
    except Exception as e:
        print(f"❌ Error creating thread: {e}")
        raise

    return thread

# ---------------------------------------------
# Retrieval of existing agent & thread
# ---------------------------------------------


def get_agent(project_client, agent_id):
    """Retrieve an existing agent using ID."""

    print("🤖 Retrieving an existing agent...")

    try:
        agent_toolset = setup_toolset()
        project_client.agents.enable_auto_function_calls(agent_toolset)

        agent = project_client.agents.get_agent(agent_id)
        if not agent or 'id' not in agent:
            print("❌ No agent found.")
            return None

        print(f"✅ Using existing agent. ID: {agent['id']}")
    except Exception as e:
        print(f"❌ Error retrieving agent: {e}")
        raise

    return agent


def get_thread(project_client, thread_id):
    """Retrieve an existing thread using ID."""

    print("🧵 Retrieve an existing conversation thread...")

    thread = project_client.agents.threads.get(thread_id)
    if not thread or 'id' not in thread:
        print("❌ No thread found.")
        return None

    print(f"✅ Using existing thread. ID: {thread['id']}")
    return thread

# ---------------------------------------------
# Get or create agent/thread helpers
# ---------------------------------------------


def _get_or_create_agent(project_client, model_deployment_name, agent_id):
    """Retrieve an existing agent by ID or create a new one if ID is not provided."""

    print("🤖 Retrieving an existing agent or creating a new one...")

    if not agent_id:
        print("🔍 AGENT_ID not found in .env. Creating a new agent...")
        try:
            agent = create_agent(project_client, model_deployment_name)
            print(
                f"⚠️ Please update your .env file with AGENT_ID: {agent.id}")
            return agent
        except Exception as e:
            print(f"❌ Error creating agent: {e}")
            raise

    print("✅ AGENT_ID found. Retrieving existing agent...")
    return get_agent(project_client, agent_id)


def _get_or_create_thread(project_client, thread_id):
    """Retrieve an existing thread by ID or create a new one if ID is not provided."""

    print("🧵 Retrieving an existing conversation thread. or creating a new one..")

    if not thread_id:
        print("🔍 THREAD_ID not found in .env. Creating a new thread...")
        try:
            thread = create_thread(project_client)
            print(
                f"⚠️ Please update your .env file with THREAD_ID: {thread.id}")
            return thread
        except Exception as e:
            print(f"❌ Error creating thread: {e}")
            raise

    print("✅ THREAD_ID found. Retrieving existing thread...")
    return get_thread(project_client, thread_id)


def get_or_create_agent_and_thread(project_client, model_deployment_name):
    """Main entry to retrieve or create agent and thread."""

    print("🤖🧵 Retrieve an existing or creating a new agent and thread..")

    agent_id = os.getenv("AGENT_ID")
    thread_id = os.getenv("THREAD_ID")
    agent = _get_or_create_agent(
        project_client, model_deployment_name, agent_id)
    thread = _get_or_create_thread(project_client, thread_id)
    return agent, thread

# ---------------------------------------------
# Message handling and processing
# ---------------------------------------------


def send_user_message(project_client, thread, user_message):
    """Send a user message to the thread."""

    print("\n📨 Sending user message to agent...")

    try:
        message = project_client.agents.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_message,
        )
        print(f"✅ Message sent! ID: {message['id']}")
    except Exception as e:
        print(f"❌ Error sending message: {e}")
        return False
    return True


def extract_tool_calls(run):
    """Extract tool call data from a run."""

    print("🛠️ Extracting tool call data from a run...")

    ra = run.required_action
    submit_tool_outputs = None
    tool_calls = []

    if ra:
        if hasattr(ra, "submit_tool_outputs"):
            submit_tool_outputs = getattr(ra, "submit_tool_outputs")
        elif isinstance(ra, dict) and "submit_tool_outputs" in ra:
            submit_tool_outputs = ra["submit_tool_outputs"]

    if submit_tool_outputs:
        if hasattr(submit_tool_outputs, "tool_calls"):
            tool_calls = submit_tool_outputs.tool_calls
        elif isinstance(submit_tool_outputs, dict) and "tool_calls" in submit_tool_outputs:
            tool_calls = submit_tool_outputs["tool_calls"]

    return tool_calls, ra


def handle_tool_output(tool_call):
    """Handle the execution of a single tool call."""

    print("🛠️ Handling the execution of a single tool call...")

    tool_name = tool_call.name
    tool_id = tool_call.id

    if tool_name == "get_company_details":
        output = get_company_details()
    else:
        return None

    return {"tool_call_id": tool_id, "output": output}


def handle_tool_calls(run, project_client, thread):
    """Run all required tools and submit their output back to the run."""

    print("🛠️ Running all required tools and submit their output back to the run...")

    tool_outputs = []
    tool_calls, ra = extract_tool_calls(run)

    if not tool_calls:
        print(f"❌ Could not access tool_calls. run.required_action: {ra}")
    for tool_call in tool_calls:
        result = handle_tool_output(tool_call)
        if result:
            tool_outputs.append(result)

    if tool_outputs:
        project_client.agents.runs.submit_tool_outputs(
            thread_id=thread.id, run_id=run.id, tool_outputs=tool_outputs
        )


def process_run(project_client, thread, agent):
    """Execute the agent and handle the run lifecycle."""

    print("🛠️ Executing the agent and handle the run lifecycle...")

    try:
        run = project_client.agents.runs.create_and_process(
            thread_id=thread.id, agent_id=agent.id
        )
        print(f"🏃 Run started! ID: {run.id}")

        while run.status in ["queued", "in_progress", "requires_action"]:
            time.sleep(1)
            run = project_client.agents.runs.get(
                thread_id=thread.id, run_id=run.id)

            if run.status == "requires_action":
                handle_tool_calls(run, project_client, thread)

        print(f"✅ Run completed with status: {run.status}")
        if run.status == "failed":
            print(f"❌ Run failed: {run.last_error}")
    except Exception as e:
        print(f"❌ Error during run: {e}")
        return False

    return True


def display_latest_assistant_message(project_client, thread):
    """Display the latest message from the assistant."""

    print("📨 Displaying the latest message from the assistant...")

    try:
        messages = project_client.agents.messages.list(thread_id=thread.id)
        recent_assistant_message = next(
            (m for m in messages if m["role"] == "assistant"), None)

        if recent_assistant_message:
            for content_item in recent_assistant_message["content"]:
                if content_item.get("type") == "text":
                    value = content_item["text"].get("value")
                    if value:
                        print(f"\n[🤖 AIAgent]: {value}\n")
    except Exception as e:
        print(f"❌ Error retrieving messages: {e}")

# ---------------------------------------------
# Optional clean-up
# ---------------------------------------------


def delete_agent(project_client, agent):
    """Delete an agent after use (optional)."""

    print("🗑️ Deleting the agent after use (optional)...")

    project_client.agents.delete_agent(agent.id)
    print("✅ Agent deleted.")


def delete_thread(project_client, thread):
    """Delete a thread after use (optional)."""

    print("🗑️ Deleting the conversational thread after use (optional)...")

    project_client.agents.threads.delete(thread_id=thread.id)
    print("✅ Thread Deleted")


# ---------------------------------------------
# Run the CLI application
# ---------------------------------------------


def run_cli():
    print("🚀 Running CLI application...")
    project_client, model_deployment_name = setup_project_client()
    agent, thread = get_or_create_agent_and_thread(
        project_client, model_deployment_name)
    print("\nType 'exit', 'q', or press Enter on an empty line to stop the conversation.\n")
    while True:
        user_message = input(
            "✨ Enter your message for the agent!\n\n[🧑 You]: ")
        if user_message.strip().lower() in ("exit", "q", ""):
            print("\n👋 Conversation ended by user.")
            break
        if not send_user_message(project_client, thread, user_message):
            continue
        if not process_run(project_client, thread, agent):
            continue
        display_latest_assistant_message(project_client, thread)

    # Optionally, delete the agent after use
    # delete_agent(project_client, agent)
    # delete_thread(project_client, thread)


if __name__ == "__main__":
    run_cli()
