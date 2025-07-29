# agents/sales_agent.py

import os
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import ConnectedAgentTool, FilePurpose, CodeInterpreterTool


def create_sales_agent(project: AIProjectClient, model_name: str, local_file_path: str):
    """
    Create a sales analysis agent with code interpreter capabilities for data analysis.

    Args:
        project: Azure AI Project client
        model_name: Name of the model deployment to use
        local_file_path: Path to the sales data file

    Returns:
        tuple: (agent, connected_tool) - The created agent and its connected tool

    Raises:
        Exception: If agent creation fails
    """
    agent_name = "sales_agent"
    agent_description = "Analyzes sales data and generates reports using Python code execution"
    agent_instructions = (
        "You are a Sales Analysis Agent with advanced data analysis capabilities. Your responsibilities include:\n"
        "- Analyzing sales performance data and trends\n"
        "- Generating comprehensive sales reports and visualizations\n"
        "- Creating charts, graphs, and statistical summaries\n"
        "- Identifying sales patterns, top performers, and growth opportunities\n"
        "- Performing comparative analysis across time periods\n"
        "- Calculating key sales metrics (revenue, conversion rates, averages, etc.)\n"
        "Use Python code to process data, create visualizations, and provide actionable insights. "
        "Always explain your analysis methodology and provide clear interpretations of results."
    )

    print(f"🤖 Creating agent ({agent_name})...")

    try:
        print(f"📁 Uploading sales data file: {local_file_path}")
        file = project.agents.files.upload(
            file_path=local_file_path, purpose=FilePurpose.AGENTS
        )
        print(f"✅ Sales data file uploaded: {file.id}")

        code_interpreter = CodeInterpreterTool(file_ids=[file.id])

        agent = project.agents.create_agent(
            model=model_name,
            name=agent_name,
            description=agent_description,
            instructions=agent_instructions,
            tools=code_interpreter.definitions,
            tool_resources=code_interpreter.resources
        )
        print(f"✅ Created {agent_name}, ID: {agent.id}")

        connected_tool = ConnectedAgentTool(
            id=agent.id,
            name=agent_name,
            description="Sales data analysis and reporting with Python code execution"
        )

        print(f"✅ {agent_name} connected to tools.")
        return agent, connected_tool

    except Exception as e:
        print(f"❌ Failed to create agent ({agent_name}): {e}")
        raise
