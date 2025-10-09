# 🧠 Inventory Management Agent (`inventory-agent-001`)

The **Inventory Management Agent** is an intelligent AI-powered assistant built using **Azure AI Projects**.
It demonstrates how to create, configure, and interact with a custom AI agent that manages company inventory, including listing items, creating new inventory entries, updating existing items, and deleting items, using integrated function tools.

## 🚀 Overview

This project sets up and runs a **custom inventory agent** using the `azure.ai.projects` SDK.
Once deployed, the agent can assist users by performing CRUD operations on a live inventory system.

The agent configuration includes:

* **Name:** `inventory-agent-001`
* **Description:** A smart AI assistant for managing inventory items with full CRUD capabilities.
* **Instructions:** Guides the agent to use tools for listing, creating, updating, or deleting inventory items accurately and safely.

## 🧩 Features

* Create or reuse an inventory agent dynamically.
* Manage threaded conversations with persistent context.
* Integrate user-defined Python tools (e.g., `get_inventory_details`, `create_inventory_item`) into the agent.
* Automatically execute and handle tool calls using Azure function tools.
* Communicate interactively with the agent via a command-line interface (CLI).
* Retrieve or delete existing agents and threads when needed.

## 📦 Prerequisites

Before running the script, make sure you have:

* **Python 3.10+**
* An **Azure account** with access to Azure AI Projects
* A **model deployment** available in your Azure environment
* Environment variables configured in a `.env` file

Example `.env` file:

```env
PROJECT_ENDPOINT=<your-azure-project-endpoint>
MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
INVENTORY_API_URI=<your-inventory-api-endpoint>
AGENT_ID=<optional-existing-agent-id>
THREAD_ID=<optional-existing-thread-id>
REQUEST_TIMEOUT=10
```

## ▶️ Running the Agent

Run the Python CLI application:

```bash
python main.py   # with Python
uv run main.py   # with uv
```

Once running, type your message to interact with the AI agent:

```md
✨ Enter your message for the agent!

[🧑 You]: List all inventory items
[🤖 InventoryAgent]: Here are all items in your inventory: ...
```

To exit the session, simply press **Enter**, type `exit`, or type `q`.

## 🧱 Script Breakdown

| Section                       | Description                                                                                               |
| ----------------------------- | --------------------------------------------------------------------------------------------------------- |
| **Environment Setup**         | Loads environment variables from `.env` and validates Azure configuration.                                |
| **AIProjectClient Setup**     | Connects to Azure AI Projects using `DefaultAzureCredential`.                                             |
| **Tool Integration**          | Loads custom Python functions (like `get_inventory_details`) into the agent using Azure’s `FunctionTool`. |
| **Agent & Thread Management** | Creates or retrieves existing agents and conversation threads.                                            |
| **Message Handling**          | Sends user prompts and receives agent responses through the Azure AI pipeline.                            |
| **Tool Execution**            | Detects when the agent needs to call a function and submits results automatically.                        |
| **CLI Interface**             | Enables interactive text-based conversation with the agent.                                               |
| **Optional Cleanup**          | Includes optional functions to delete agents and threads after testing.                                   |

## 🧠 Agent Configuration

```python
agent_name: str = "inventory-agent-001"

agent_description: str = (
    "A smart inventory management assistant designed to handle company stock. "
    "It can list all items, create new inventory entries, update existing items, "
    "and delete items using live API integration."
)

agent_instructions: str = (
    "You are an expert inventory assistant. Use the available tools to "
    "accurately list, create, update, or delete inventory items. "
    "Always confirm actions before making permanent changes and respond clearly."
)
```

## 🧰 Tools and Functions

The agent includes a **custom toolset** defined in `tools.py`:

```python
def get_inventory_details():
    """Return all items in inventory as JSON string."""
    ...

def get_inventory_item(item_id):
    """Return a single item by ID as JSON string."""
    ...

def create_inventory_item(name, price, quantity, description=None):
    """Create a new item and return JSON string of created item."""
    ...

def update_inventory_item(item_id, name=None, price=None, quantity=None, description=None):
    """Update an existing item and return JSON string of updated item."""
    ...

def delete_inventory_item(item_id):
    """Delete an item by ID and return JSON string result."""
    ...
```

These functions allow the agent to interact dynamically with the inventory API when users request actions.

## 🧹 Cleanup (Optional)

After testing, you can delete the agent and thread to reset the environment:

```python
delete_agent(project_client, agent)
delete_thread(project_client, thread)
```

## 🪄 Example Use Cases

* List all inventory items
* Retrieve details of a specific item
* Add a new item to inventory
* Update existing inventory entries
* Remove items from inventory
* Support internal inventory management workflows
