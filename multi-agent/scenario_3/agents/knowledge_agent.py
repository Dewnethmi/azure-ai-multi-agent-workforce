# agents/knowledge_agent.py

from azure.ai.agents.models import ConnectedAgentTool, FilePurpose, FileSearchTool


def upload_file_and_create_vector_store(project, file_path):
    """
    Upload a company knowledge file and create a vector store for search functionality.

    Args:
        project: Azure AI Project client
        file_path: Path to the company knowledge file

    Returns:
        vector_store: Created vector store with uploaded file

    Raises:
        Exception: If file upload or vector store creation fails
    """
    try:
        print(f"📁 Uploading knowledge file: {file_path}")
        file = project.agents.files.upload(
            file_path=file_path, purpose=FilePurpose.AGENTS
        )
        print(f"✅ File uploaded: {file.id}")

        print("🔍 Creating vector store...")
        vector_store = project.agents.vector_stores.create_and_poll(
            file_ids=[file.id], name="company_knowledge_vectorstore"
        )
        print(f"✅ Vector store created: {vector_store.id}")

        return vector_store

    except Exception as e:
        print(f"❌ Failed to upload file or create vector store: {e}")
        raise


def create_knowledge_agent(project, model_name, file_path):
    """
    Create a knowledge agent with file search capabilities for company information.

    Args:
        project: Azure AI Project client
        model_name: Name of the model deployment to use
        file_path: Path to the company knowledge file

    Returns:
        tuple: (agent, connected_tool) - The created agent and its connected tool

    Raises:
        Exception: If agent creation fails
    """
    agent_name = "knowledge_agent"
    agent_description = "Provides company business logic, policies, and organizational information"
    agent_instructions = (
        "You are a Company Knowledge Agent. You have access to comprehensive company information including:\n"
        "- Business policies and procedures\n"
        "- Company guidelines and rules\n"
        "- Organizational structure and contacts\n"
        "- Standard operating procedures\n"
        "- Company history and culture\n"
        "Use the file search tool to find accurate, up-to-date information from company documents. "
        "Always provide clear, authoritative answers based on official company documentation."
    )

    print(f"🤖 Creating ({agent_name})...")

    try:
        vector_store = upload_file_and_create_vector_store(project, file_path)
        file_search_tool = FileSearchTool(vector_store_ids=[vector_store.id])

        agent = project.agents.create_agent(
            model=model_name,
            name=agent_name,
            description=agent_description,
            instructions=agent_instructions,
            tools=file_search_tool.definitions,
            tool_resources=file_search_tool.resources,
        )

        print(f"✅ {agent_name} created: {agent.id}")

        connected_tool = ConnectedAgentTool(
            id=agent.id,
            name=agent_name,
            description="Provides company business logic, policies, and organizational knowledge"
        )

        print(f"✅ {agent_name} connected to tools.")
        return agent, connected_tool

    except Exception as e:
        print(f"❌ Failed to create agent ({agent_name}): {e}")
        raise
