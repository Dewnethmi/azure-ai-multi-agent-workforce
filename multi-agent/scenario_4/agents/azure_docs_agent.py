# agents/azure_docs_agent.py

import os
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import McpTool, ConnectedAgentTool


def create_azure_docs_agent(project: AIProjectClient, model_name: str):
    """
    Create an Azure documentation agent with MCP tools for Azure REST API documentation.

    Args:
        project: Azure AI Project client
        model_name: Name of the model deployment to use

    Returns:
        tuple: (agent, connected_tool) - The created agent and its connected tool

    Raises:
        Exception: If agent creation fails
    """
    agent_name = "azure_docs_agent"
    agent_description = "Specialized agent for Azure REST API documentation and specifications"
    agent_instructions = (
        "You are an Azure Documentation Agent, specialized in accessing and analyzing Azure REST API documentation. "
        "Your primary capabilities include:\n\n"

        "**Core Responsibilities:**\n"
        "- Searching and analyzing Azure REST API specifications\n"
        "- Retrieving detailed documentation about Azure services and APIs\n"
        "- Providing accurate information from official Azure documentation sources\n"
        "- Finding code examples and implementation details\n"
        "- Accessing Azure service schemas and data models\n\n"

        "**Available Tools:**\n"
        "- Azure REST API specifications search (search_azure_rest_api_code)\n"
        "- Access to comprehensive Azure documentation repository\n"
        "- Real-time documentation retrieval from official sources\n\n"

        "**Response Guidelines:**\n"
        "- Always search the Azure documentation when asked about specific APIs or services\n"
        "- Provide accurate, up-to-date information from official sources\n"
        "- Include relevant code snippets and examples when available\n"
        "- Cite specific documentation sections when referencing features\n"
        "- If information is not found, clearly state this and suggest alternatives\n\n"

        "Focus on providing comprehensive, accurate Azure documentation and API information!"
    )

    print(f"🤖 Creating agent ({agent_name})...")

    try:
        # Get MCP server configuration from environment variables
        mcp_server_url = os.environ.get(
            "MCP_SERVER_URL_AZURE_REST", "https://gitmcp.io/Azure/azure-rest-api-specs")
        mcp_server_label = os.environ.get("MCP_SERVER_LABEL", "github")

        print(
            f"🔗 Configuring MCP server: {mcp_server_label} at {mcp_server_url}")

        # Initialize agent MCP tool
        mcp_tool = McpTool(
            server_label=mcp_server_label,
            server_url=mcp_server_url,
            allowed_tools=[],  # Optional: specify allowed tools
        )

        # Add allowed tools for Azure documentation search
        search_api_code = "search_azure_rest_api_code"
        mcp_tool.allow_tool(search_api_code)

        print(f"🔧 Configured MCP tools: {mcp_tool.allowed_tools}")

        # Update headers if needed
        mcp_tool.update_headers("User-Agent", "AzureDocsAgent/1.0")

        agent = project.agents.create_agent(
            model=model_name,
            name=agent_name,
            description=agent_description,
            instructions=agent_instructions,
            tools=mcp_tool.definitions,
            tool_resources=mcp_tool.resources
        )
        print(f"✅ Created {agent_name}, ID: {agent.id}")

        connected_tool = ConnectedAgentTool(
            id=agent.id,
            name=agent_name,
            description="Azure REST API documentation search and analysis with MCP tools"
        )

        print(f"✅ {agent_name} connected as tool.")
        return agent, connected_tool

    except Exception as e:
        print(f"❌ Failed to create agent ({agent_name}): {e}")
        print("💡 Make sure MCP_SERVER_URL_AZURE_REST and MCP_SERVER_LABEL environment variables are set")
        raise
