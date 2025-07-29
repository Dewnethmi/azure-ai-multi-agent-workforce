# agents/store_manager_agent.py


def create_main_agent(project, model_name, knowledge_agent_tool, inventory_agent_tool, sales_agent_tool):
    """
    Create the main store manager agent that coordinates with all other specialized agents.

    Args:
        project: Azure AI Project client
        model_name: Name of the model deployment to use
        knowledge_agent_tool: Connected tool for company knowledge agent
        inventory_agent_tool: Connected tool for inventory management agent
        sales_agent_tool: Connected tool for sales analysis agent

    Returns:
        agent: The created store manager agent

    Raises:
        Exception: If agent creation fails
    """
    agent_name = "store_manager_agent"
    agent_description = "Main orchestrator for inventory management system operations"
    agent_instructions = (
        "You are the Store Manager, the main coordinator for our inventory management system. "
        "You have access to three specialized agents to help you:\n\n"

        "1. **Knowledge Agent**: For company policies, business rules, and organizational information\n"
        "   - Use when users ask about company procedures, policies, or general business information\n\n"

        "2. **Inventory Agent**: For all inventory-related operations\n"
        "   - Use for checking stock levels, product availability, adding/updating/deleting items\n"
        "   - Handles all CRUD operations for inventory management\n\n"

        "3. **Sales Agent**: For sales analysis and reporting\n"
        "   - Use for sales performance analysis, generating reports, and data visualization\n"
        "   - Handles trend analysis and sales metrics calculations\n\n"

        "**Your Role:**\n"
        "- Route user queries to the appropriate specialized agent\n"
        "- Coordinate responses from multiple agents when needed\n"
        "- Provide comprehensive answers by combining information from different sources\n"
        "- Maintain a professional, helpful tone focused on inventory and business management\n"
        "- Always ensure users get accurate, up-to-date information about inventory status, company policies, and sales performance\n\n"

        "When users ask questions, determine which agent(s) can best help and coordinate their responses effectively."
    )

    print(f"🤖 Creating ({agent_name})...")

    try:
        # Combine all connected agent tools
        all_tools = (knowledge_agent_tool.definitions +
                     inventory_agent_tool.definitions +
                     sales_agent_tool.definitions)

        agent = project.agents.create_agent(
            model=model_name,
            name=agent_name,
            description=agent_description,
            instructions=agent_instructions,
            tools=all_tools,
        )

        print(f"✅ {agent_name} created: {agent.id}")
        print(f"🔗 Connected to {len(all_tools)} specialized tools")
        return agent

    except Exception as e:
        print(f"❌ Failed to create agent ({agent_name}): {e}")
        raise
