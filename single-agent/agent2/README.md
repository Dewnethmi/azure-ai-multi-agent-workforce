# 🧠 Inventory Management Agent (`inventory-management-agent-001`)

The **Inventory Management Agent** is an intelligent AI-powered assistant built using **Azure AI Projects**.
It demonstrates how to create, configure, and interact with a custom AI agent that can manage and provide insights about company inventory, stock levels, and related details using integrated function tools.

## 🚀 Overview

This project sets up and runs a **custom inventory management agent** using the `azure.ai.projects` SDK.
Once deployed, the agent can assist users by retrieving company details, answering questions about inventory operations, and supporting decision-making related to product stock and availability.

The agent configuration includes:

* **Name:** `inventory-management-agent-001`
* **Description:** An intelligent inventory management assistant for tracking and optimizing product stock.
* **Instructions:** Guides the agent to provide accurate, clear, and professional responses about inventory data and company information.

## 🧩 Features

* Create or reuse an inventory management agent dynamically.
* Manage threaded conversations with persistent context.
* Integrate user-defined Python tools (e.g., `get_company_details`) into the agent.
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
AGENT_ID=<optional-existing-agent-id>
THREAD_ID=<optional-existing-thread-id>
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

[🧑 You]: Show me the company details
[🤖 AIAgent]: Our company, Tech Supplies Co., is located at 123 Innovation Drive,...
```

To exit the session, simply press **Enter**, type `exit`, or type `q`.

## 🧱 Script Breakdown

| Section                       | Description                                                                                             |
| ----------------------------- | ------------------------------------------------------------------------------------------------------- |
| **Environment Setup**         | Loads environment variables from `.env` and validates Azure configuration.                              |
| **AIProjectClient Setup**     | Connects to Azure AI Projects using `DefaultAzureCredential`.                                           |
| **Tool Integration**          | Loads custom Python functions (like `get_company_details`) into the agent using Azure’s `FunctionTool`. |
| **Agent & Thread Management** | Creates or retrieves existing agents and conversation threads.                                          |
| **Message Handling**          | Sends user prompts and receives agent responses through the Azure AI pipeline.                          |
| **Tool Execution**            | Detects when the agent needs to call a function and submits results automatically.                      |
| **CLI Interface**             | Enables interactive text-based conversation with the agent.                                             |
| **Optional Cleanup**          | Includes optional functions to delete agents and threads after testing.                                 |

## 🧠 Agent Configuration

```python
agent_name: str = "inventory-management-agent-001"

agent_description: str = (
    "An intelligent inventory management assistant designed to help users track, manage, "
    "and optimize product stock across various locations. It can provide insights, updates, "
    "and support related to inventory levels, product availability, and restocking needs."
)

agent_instructions: str = (
    "You are an expert inventory management assistant. Help users monitor and manage "
    "inventory efficiently by answering questions, providing stock information, generating summaries, "
    "and offering recommendations. Always ensure accuracy and clarity in your responses, "
    "and maintain a professional, supportive tone when assisting users."
)
```

## 🧰 Tools and Functions

The agent includes a **custom toolset** defined in `tools.py`:

```python
def get_company_details():
    return {
        "name": "Tech Supplies Co.",
        "address": "123 Innovation Drive, Tech City",
        "contact": "+94123456789",
        "email": "contact@dileepa.dev",
        "website": "https://tech-inventory.dileepa.dev",
        "privacy_policy": "https://tech-inventory.dileepa.dev/privacy-policy",
        "terms_and_conditions": "https://tech-inventory.dileepa.dev/terms-and-conditions",
        "mission": "To provide high-quality tech supplies to businesses worldwide.",
        "vision": "To be the leading supplier of innovative tech solutions.",
        "values": [
            "Customer Satisfaction",
            "Innovation",
            "Integrity",
            "Sustainability"
        ]
    }
```

This function allows the agent to retrieve company information dynamically when users request it.

## 🧹 Cleanup (Optional)

After testing, you can delete the agent and thread to reset the environment:

```python
delete_agent(project_client, agent)
delete_thread(project_client, thread)
```

## 🪄 Example Use Cases

* Retrieve company and product information
* Manage or summarize inventory stock data
* Support queries about item availability
* Automate responses to customer inquiries
* Provide operational insights for warehouse teams
