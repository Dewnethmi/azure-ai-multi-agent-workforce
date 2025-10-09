import os
import time
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import FunctionTool, ToolSet
from tools import (
    get_inventory_details,
    create_inventory_item,
    get_inventory_item,
    update_inventory_item,
    delete_inventory_item,
)

# ---------------------------------------------
# Load environment variables
# ---------------------------------------------
print("🔄 Loading environment variables...")
load_dotenv()

# ---------------------------------------------
# Project setup functions
# ---------------------------------------------


def setup_project_client():
    """Initialize AIProjectClient with credentials and environment variables."""
    PROJECT_ENDPOINT = os.getenv("PROJECT_ENDPOINT")
    MODEL_DEPLOYMENT_NAME = os.getenv("MODEL_DEPLOYMENT_NAME")

    if not PROJECT_ENDPOINT or not MODEL_DEPLOYMENT_NAME:
        raise ValueError(
            "❌ PROJECT_ENDPOINT or MODEL_DEPLOYMENT_NAME missing in .env")

    print("🔗 Connecting to Azure AI Project...")
    try:
        project_client = AIProjectClient(
            endpoint=PROJECT_ENDPOINT, credential=DefaultAzureCredential())
        print("✅ Connected to Azure AI Project!")
    except Exception as e:
        print(f"❌ Error initializing AIProjectClient: {e}")
        raise
    return project_client, MODEL_DEPLOYMENT_NAME


def setup_toolset():
    """Define inventory API functions as FunctionTool and return a ToolSet."""
    print("🛠️ Setting up agent toolset...")
    user_functions = {
        get_inventory_details,
        create_inventory_item,
        get_inventory_item,
        update_inventory_item,
        delete_inventory_item,
    }
    functions = FunctionTool(user_functions)
    toolset = ToolSet()
    toolset.add(functions)
    print(f"✅ Toolset defined: {toolset}")
    return toolset

# ---------------------------------------------
# Agent & thread creation/retrieval
# ---------------------------------------------


def create_agent(project_client, model_name):
    print("🤖 Creating a new agent...")
    agent_toolset = setup_toolset()
    project_client.agents.enable_auto_function_calls(agent_toolset)
    agent = project_client.agents.create_agent(
        model=model_name,
        name="inventory-agent-001",
        instructions=(
            "You are an inventory assistant with access to a live inventory API. "
            "Use the tools to list, create, update, or delete items accurately. "
            "Always confirm actions before making permanent changes."
        ),
        description="Advanced inventory agent with full CRUD capabilities",
        toolset=agent_toolset,
    )
    print(f"✅ Agent created! ID: {agent.id}")
    return agent


def create_thread(project_client):
    print("🧵 Creating a new conversation thread...")
    thread = project_client.agents.threads.create()
    print(f"✅ Thread created! ID: {thread.id}")
    return thread


def get_agent(project_client, agent_id):
    print("🤖 Retrieving existing agent...")
    agent_toolset = setup_toolset()
    project_client.agents.enable_auto_function_calls(agent_toolset)
    agent = project_client.agents.get_agent(agent_id)
    if not agent or "id" not in agent:
        print("❌ No agent found.")
        return None
    print(f"✅ Using existing agent. ID: {agent['id']}")
    return agent


def get_thread(project_client, thread_id):
    print("🧵 Retrieving existing thread...")
    thread = project_client.agents.threads.get(thread_id)
    if not thread or "id" not in thread:
        print("❌ No thread found.")
        return None
    print(f"✅ Using existing thread. ID: {thread['id']}")
    return thread


def _get_or_create_agent(project_client, model_name, agent_id):
    if not agent_id:
        print("🔍 AGENT_ID not found. Creating new agent...")
        agent = create_agent(project_client, model_name)
        print(f"⚠️ Update .env with AGENT_ID={agent.id}")
        return agent
    return get_agent(project_client, agent_id)


def _get_or_create_thread(project_client, thread_id):
    if not thread_id:
        print("🔍 THREAD_ID not found. Creating new thread...")
        thread = create_thread(project_client)
        print(f"⚠️ Update .env with THREAD_ID={thread.id}")
        return thread
    return get_thread(project_client, thread_id)


def get_or_create_agent_and_thread(project_client, model_name):
    agent_id = os.getenv("AGENT_ID")
    thread_id = os.getenv("THREAD_ID")
    agent = _get_or_create_agent(project_client, model_name, agent_id)
    thread = _get_or_create_thread(project_client, thread_id)
    return agent, thread

# ---------------------------------------------
# Messaging & tool call handling
# ---------------------------------------------


def send_user_message(project_client, thread, user_message):
    try:
        project_client.agents.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_message,
        )
    except Exception as e:
        print(f"❌ Error sending message: {e}")
        return False
    return True


def extract_tool_calls(run):
    ra = run.required_action
    submit_tool_outputs = getattr(ra, "submit_tool_outputs", None)
    tool_calls = getattr(submit_tool_outputs, "tool_calls",
                         []) if submit_tool_outputs else []
    return tool_calls, ra


def handle_tool_output(tool_call):
    tool_name = tool_call.name
    tool_id = tool_call.id
    params = getattr(tool_call, "parameters", {})

    if tool_name == "get_inventory_details":
        output = get_inventory_details()
    elif tool_name == "get_inventory_item":
        output = get_inventory_item(params.get("item_id"))
    elif tool_name == "create_inventory_item":
        output = create_inventory_item(
            name=params.get("name"),
            price=params.get("price"),
            quantity=params.get("quantity"),
            description=params.get("description")
        )
    elif tool_name == "update_inventory_item":
        output = update_inventory_item(
            item_id=params.get("item_id"),
            name=params.get("name"),
            price=params.get("price"),
            quantity=params.get("quantity"),
            description=params.get("description")
        )
    elif tool_name == "delete_inventory_item":
        output = delete_inventory_item(params.get("item_id"))
    else:
        return None

    return {"tool_call_id": tool_id, "output": output}


def handle_tool_calls(run, project_client, thread):
    tool_calls, ra = extract_tool_calls(run)
    if not tool_calls:
        print(f"❌ No tool calls found. run.required_action: {ra}")
        return

    tool_outputs = []
    for tool_call in tool_calls:
        result = handle_tool_output(tool_call)
        if result:
            tool_outputs.append(result)

    if tool_outputs:
        project_client.agents.runs.submit_tool_outputs(
            thread_id=thread.id, run_id=run.id, tool_outputs=tool_outputs
        )


def process_run(project_client, thread, agent):
    try:
        run = project_client.agents.runs.create_and_process(
            thread_id=thread.id, agent_id=agent.id)
        while run.status in ["queued", "in_progress", "requires_action"]:
            time.sleep(1)
            run = project_client.agents.runs.get(
                thread_id=thread.id, run_id=run.id)
            if run.status == "requires_action":
                handle_tool_calls(run, project_client, thread)
        if run.status == "failed":
            print(f"❌ Run failed: {run.last_error}")
            return False
    except Exception as e:
        print(f"❌ Error during run: {e}")
        return False
    return True


def display_latest_assistant_message(project_client, thread):
    messages = project_client.agents.messages.list(thread_id=thread.id)
    recent = next((m for m in messages if m["role"] == "assistant"), None)
    if recent:
        for c in recent["content"]:
            if c.get("type") == "text":
                value = c["text"]["value"]
                if value:
                    print(f"\n[🤖 InventoryAgent]: {value}\n")

# ---------------------------------------------
# CLI
# ---------------------------------------------


def run_cli():
    client, model_name = setup_project_client()
    agent, thread = get_or_create_agent_and_thread(client, model_name)

    print("\nType 'exit', 'q', or Enter on empty line to quit.\n")
    while True:
        msg = input("[🧑 You]: ")
        if msg.strip().lower() in ("exit", "q", ""):
            break
        if not send_user_message(client, thread, msg):
            continue
        if not process_run(client, thread, agent):
            continue
        display_latest_assistant_message(client, thread)


if __name__ == "__main__":
    run_cli()
