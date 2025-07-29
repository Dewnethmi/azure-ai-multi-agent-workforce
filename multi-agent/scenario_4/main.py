# main.py

import sys
from settings import load_configuration
from core.azure_client import connect_to_project
from core.cleanup_utils import delete_agents
from agents.azure_docs_agent import create_azure_docs_agent
from agents.study_buddy_agent import create_study_buddy_agent
from core.conversation_manager import (
    create_thread,
    send_user_message,
    run_agent,
    display_agent_responses
)


def create_study_system(project, model_name):
    """
    Create and initialize the complete study buddy system with all agents.

    Args:
        project: Azure AI Project client
        model_name: Name of the model deployment to use

    Returns:
        tuple: All created agents (azure_docs_agent, study_buddy_agent)
    """
    try:
        print("")
        print("🏗️ Building Study Buddy System...")

        azure_docs_agent, azure_docs_agent_tool = create_azure_docs_agent(
            project, model_name)
        study_buddy_agent = create_study_buddy_agent(
            project, model_name, azure_docs_agent_tool)

        print("✅ Study buddy system ready!")
        return azure_docs_agent, study_buddy_agent

    except Exception as e:
        print(f"❌ Failed to create study system: {e}")
        raise


def interactive_session(project, study_buddy_agent):
    """
    Start an interactive chat session with the study buddy agent.

    Args:
        project: Azure AI Project client
        study_buddy_agent: The main study buddy agent
    """
    try:
        thread = create_thread(project)

        print("\n🎉 Welcome to your Azure Documentation Study Buddy!")
        print("Ask me about Azure REST API specifications, documentation, or any Azure-related questions.")
        print("Type 'quit' to exit.\n")

        while True:
            try:
                user_input = input("👤 You: ").strip()

                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("👋 Thanks for using the Study Buddy System!")
                    break

                if not user_input:
                    continue

                send_user_message(project, thread, user_input)
                run = run_agent(project, thread, study_buddy_agent)
                display_agent_responses(project, thread, run)
                print()

            except KeyboardInterrupt:
                print("\n👋 Session ended. Happy studying!")
                break
            except Exception as e:
                print(f"❌ Error during conversation: {e}")
                continue

    except Exception as e:
        print(f"❌ Failed to start interactive session: {e}")
        raise


def demo_session(project, study_buddy_agent):
    """
    Run a demo session with predefined questions for the study buddy system.

    Args:
        project: Azure AI Project client
        study_buddy_agent: The main study buddy agent
    """
    try:
        thread = create_thread(project)

        demo_questions = [
            "Hi! Can you help me understand Azure REST APIs?",
        ]

        # This is another example
        # demo_questions = [
        #     "Hi! Can you help me understand Azure REST APIs?",
        #     "Please summarize the Azure REST API specifications Readme",
        #     "What are the key components of Azure Resource Manager APIs?",
        #     "How do I authenticate with Azure REST APIs?",
        #     "What are the best practices for Azure API development?"
        # ]

        print("\n🎬 Running Study Buddy Demo Session...")
        print("=" * 50)

        for question in demo_questions:
            try:
                print(f"\n💭 Demo Question: {question}")
                print("-" * 40)

                send_user_message(project, thread, question)
                run = run_agent(project, thread, study_buddy_agent)
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
    Main entry point for the study buddy system.
    """
    try:
        print("🚀 Starting Study Buddy System...")

        endpoint, model_name = load_configuration()
        project = connect_to_project(endpoint)

        _, study_buddy_agent = create_study_system(
            project, model_name)

        print("\nSelect session type:")
        print("1. Interactive session (chat with the study buddy)")
        print("2. Demo session (see predefined examples)")

        choice = input("Enter choice (1 or 2): ").strip()

        if choice == "1":
            interactive_session(project, study_buddy_agent)
        elif choice == "2":
            demo_session(project, study_buddy_agent)
        else:
            print("Running demo session by default...")
            demo_session(project, study_buddy_agent)

        # Optional cleanup (uncomment if needed)
        # print("\n🧹 Cleaning up agents...")
        # delete_agents(project, study_buddy_agent, azure_docs_agent)

        print("🎉 Study Buddy System session completed!")

    except KeyboardInterrupt:
        print("\n🛑 Program interrupted by user")
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        sys.exit(1)
    finally:
        print("🔴 Program terminated")


if __name__ == "__main__":
    main()
