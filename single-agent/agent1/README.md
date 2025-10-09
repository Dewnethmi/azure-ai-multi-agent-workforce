# 🧠 General Writing Agent (`general-writing-agent-001`)

The **General Writing Agent** is an AI-powered writing assistant built using **Azure AI Projects**.
It demonstrates how to create, configure, and interact with a custom AI agent capable of drafting, editing, summarizing, and refining text across various writing styles.

## 🚀 Overview

This project sets up and runs a **custom writing agent** using the `azure.ai.projects` SDK.
Once deployed, the agent can process user messages — for example, writing poems, improving documents, or generating creative text.

The agent configuration includes:

* **Name:** `general-writing-agent-001`
* **Description:** An intelligent writing assistant for clear, coherent, and stylistically refined text.
* **Instructions:** Guides the agent to write and edit content with precision, clarity, and tone alignment.

## 🧩 Features

* Create and configure a writing agent dynamically.
* Initiate and manage threaded conversations with users.
* Send user prompts and receive AI-generated responses.
* Integrate with Azure’s authentication via `DefaultAzureCredential`.
* View responses directly in the terminal.

## 📦 Prerequisites

Before running the script, make sure you have:

* **Python 3.10+**
* An **Azure account** with access to Azure AI Projects.
* A **model deployment** available in your Azure environment.

## ▶️ Running the Agent

Run the Python script:

```bash
python main.py # with Python
uv run main.py # with uv
```

Expected output:

* Environment variables loaded
* Azure AI Project connected
* Agent created and configured
* Thread started and user message sent
* Agent response displayed in the console

Example:

```md
💬 User message: Write me a poem about flowers
🧠 Assistant: Gentle blooms in morning light, whisper dreams in colors bright...
```

## 🧱 Script Breakdown

| Section                        | Description                                                                 |
| ------------------------------ | --------------------------------------------------------------------------- |
| **Environment Setup**          | Loads variables from `.env` and validates configuration.                    |
| **AIProjectClient Connection** | Connects to Azure AI Project using `DefaultAzureCredential`.                |
| **Agent Configuration**        | Defines the agent’s name, description, and behavioral instructions.         |
| **Message Handling**           | Creates conversation threads, sends user messages, and retrieves responses. |
| **Run Execution**              | Processes a single run to generate the AI’s reply.                          |
| **Optional Cleanup**           | Code is provided to delete the agent if desired.                            |

## 🧠 Agent Configuration

```python
agent_name = "general-writing-agent-001"

agent_description = (
    "An intelligent writing assistant capable of drafting, editing, summarizing, "
    "and refining various types of written content with clarity, tone, and coherence."
)

agent_instructions = (
    "You are an expert writing assistant. Help users craft high-quality content across "
    "different formats — including articles, essays, blogs, documentation, and creative writing. "
    "Focus on clarity, style, and accuracy while maintaining the user's intended tone and purpose. "
    "When editing or rewriting, explain your reasoning concisely if asked."
)
```

## 🧹 Cleanup (Optional)

You can delete the agent after testing:

```python
project.agents.delete_agent(agent.id)
```

## 🪄 Example Use Cases

* Blog and article drafting
* Technical documentation cleanup
* Marketing copy improvement
* Story or poem generation
* Grammar and tone refinement
