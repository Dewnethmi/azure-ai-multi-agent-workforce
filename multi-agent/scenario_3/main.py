# main.py

import sys
from settings import load_configuration
from core.azure_client import connect_to_project
from core.cleanup_utils import delete_agents
from agents.knowledge_agent import create_knowledge_agent
from agents.inventory_agent import create_inventory_agent
from agents.sales_agent import create_sales_agent
from agents.store_manager_agent import create_main_agent
from core.conversation_manager import (
    create_thread,
    send_user_message,
    run_agent,
    display_agent_responses
)


def create_inventory_system(project, model_name):
    """
    Create and initialize the complete inventory management system with all agents.

    Args:
        project: Azure AI Project client
        model_name: Name of the model deployment to use

    Returns:
        tuple: All created agents (knowledge, inventory, sales, store_manager)
    """
    try:
        print("")
        print("🏗️ Building Inventory Management System...")

        knowledge_agent, knowledge_agent_tool = create_knowledge_agent(
            project, model_name, './data/company.md')
        inventory_agent, inventory_agent_tool = create_inventory_agent(
            project, model_name)
        sales_agent, sales_agent_tool = create_sales_agent(
            project, model_name, './data/sales_data.csv')
        store_manager_agent = create_main_agent(
            project, model_name, knowledge_agent_tool, inventory_agent_tool, sales_agent_tool)

        print("✅ Inventory management system ready!")
        return knowledge_agent, inventory_agent, sales_agent, store_manager_agent

    except Exception as e:
        print(f"❌ Failed to create inventory system: {e}")
        raise


def interactive_session(project, store_manager_agent):
    """
    Start an interactive chat session with the store manager agent.

    Args:
        project: Azure AI Project client
        store_manager_agent: The main store manager agent
    """
    try:
        thread = create_thread(project)

        print("\n🎉 Welcome to your Inventory Management System!")
        print("Ask me about inventory, company policies, sales analysis, or product availability.")
        print("Type 'quit' to exit.\n")

        while True:
            try:
                user_input = input("👤 You: ").strip()

                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("👋 Thanks for using the Inventory Management System!")
                    break

                if not user_input:
                    continue

                send_user_message(project, thread, user_input)
                run = run_agent(project, thread, store_manager_agent)
                display_agent_responses(project, thread, run)
                print()

            except KeyboardInterrupt:
                print("\n👋 Session ended. Have a great day!")
                break
            except Exception as e:
                print(f"❌ Error during conversation: {e}")
                continue

    except Exception as e:
        print(f"❌ Failed to start interactive session: {e}")
        raise


def demo_session(project, store_manager_agent):
    """
    Run a demo session with predefined questions for the inventory system.

    Args:
        project: Azure AI Project client
        store_manager_agent: The main store manager agent
    """
    try:
        thread = create_thread(project)

        demo_questions = [
            "Hi! Are there any apples in stock?",
            "What's our company policy on returns?",
            "Can you analyze last month's sales performance?",
            "Show me all available products",
            "What are the top selling items?"
        ]

        print("\n🎬 Running Inventory Management Demo Session...")
        print("=" * 50)

        for question in demo_questions:
            try:
                print(f"\n💭 Demo Question: {question}")
                print("-" * 40)

                send_user_message(project, thread, question)
                run = run_agent(project, thread, store_manager_agent)
                display_agent_responses(project, thread, run)
                print()

            except Exception as e:
                print(f"❌ Error processing demo question '{question}': {e}")
                continue

    except Exception as e:
        print(f"❌ Failed to run demo session: {e}")
        raise


def main():
    """
    Main entry point for the inventory management system.
    """
    try:
        print("🚀 Starting Inventory Management System...")

        endpoint, model_name = load_configuration()
        project = connect_to_project(endpoint)

        _, _, _, store_manager_agent = create_inventory_system(
            project, model_name)

        print("\nSelect session type:")
        print("1. Interactive session (chat with the system)")
        print("2. Demo session (see predefined examples)")

        choice = input("Enter choice (1 or 2): ").strip()

        if choice == "1":
            interactive_session(project, store_manager_agent)
        elif choice == "2":
            demo_session(project, store_manager_agent)
        else:
            print("Running demo session by default...")
            demo_session(project, store_manager_agent)

        # Optional cleanup (uncomment if needed)
        # print("\n🧹 Cleaning up agents...")
        # delete_agents(project, store_manager_agent, knowledge_agent, inventory_agent, sales_agent)

        print("🎉 Inventory Management System session completed!")

    except KeyboardInterrupt:
        print("\n🛑 Program interrupted by user")
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        sys.exit(1)
    finally:
        print("🔴 Program terminated")


if __name__ == "__main__":
    main()
