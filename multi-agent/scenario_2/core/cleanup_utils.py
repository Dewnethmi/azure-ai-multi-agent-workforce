import logging


def delete_agents(project, *agents):
    """Clean up agents after execution (optional)."""
    logging.info("🗑️ Starting agent cleanup process...")

    for agent in agents:
        try:
            logging.info(f"🗑️ Deleting agent: {agent.name}")
            project.agents.delete_agent(agent.id)
            logging.info(f"✅ Deleted agent: {agent.name}")
        except Exception as e:
            logging.error(f"❌ Failed to delete agent {agent.name}: {e}")

    logging.info("✅ Agent cleanup process completed.")
