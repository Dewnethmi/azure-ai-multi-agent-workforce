# core/cleanup_utils.py

def delete_agents(project, *agents):
    """
    Clean up agents after execution by deleting them from the project.

    Args:
        project: Azure AI Project client
        *agents: Variable number of agent objects to delete

    Note:
        This function will attempt to delete all provided agents, continuing
        even if some deletions fail, and will report the status of each deletion.
    """
    if not agents:
        print("⚠️ No agents provided for cleanup")
        return

    print("🗑️ Starting agent cleanup process...")

    deleted_count = 0
    failed_count = 0

    for agent in agents:
        try:
            if hasattr(agent, 'name') and hasattr(agent, 'id'):
                agent_name = getattr(agent, 'name', 'Unknown')
                agent_id = getattr(agent, 'id', 'Unknown')

                print(f"🗑️ Deleting agent: {agent_name} (ID: {agent_id})")
                project.agents.delete_agent(agent.id)
                print(f"✅ Deleted agent: {agent_name}")
                deleted_count += 1
            else:
                print(f"⚠️ Skipping invalid agent object: {agent}")
                failed_count += 1

        except Exception as e:
            agent_name = getattr(agent, 'name', 'Unknown')
            print(f"❌ Failed to delete agent {agent_name}: {e}")
            failed_count += 1

    print(
        f"✅ Agent cleanup completed. Deleted: {deleted_count}, Failed: {failed_count}")

    if failed_count > 0:
        print("⚠️ Some agents could not be deleted. They may need manual cleanup.")
