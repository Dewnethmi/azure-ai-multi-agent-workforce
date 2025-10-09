# 🧠 Company Information Agent (`company-info-agent-001`)

The **Company Information Agent** is an intelligent AI-powered assistant built using **Azure AI Projects**.
It demonstrates how to create, configure, and interact with a custom AI agent that provides comprehensive company details, including contact info, mission, vision, values, and legal policies, using integrated function tools.

## 🚀 Overview

This project sets up and runs a **custom company information agent** using the `azure.ai.projects` SDK.
Once deployed, the agent can assist users by retrieving company details and answering questions about the organization’s policies, goals, and general information.

The agent configuration includes:

* **Name:** `company-info-agent-001`
* **Description:** A smart AI assistant for providing company-related details to users.
* **Instructions:** Guides the agent to provide accurate, clear, and professional responses about the company.

## 🧩 Features

* Create or reuse a company information agent dynamically.
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

* Retrieve company contact information
* Access mission, vision, and core values
* Provide legal policy details (privacy, terms)
* Answer general questions about the organization
* Support internal or external informational requests
