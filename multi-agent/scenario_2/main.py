#!/usr/bin/env python3
"""
🏋️ Fitness & Wellness Advisor - Multi-Agent System
=================================================

A comprehensive wellness advisor using Azure AI Foundry connected agents:
- FitAgent: Main wellness coordinator
- DietAgent: Nutrition and meal planning specialist  
- WorkoutAgent: Fitness training and exercise specialist

Usage: python main.py
"""

import sys
from settings import setup_logging, load_configuration
from core.azure_client import connect_to_project
from core.cleanup_utils import delete_agents
from agents.diet_agent import create_diet_agent
from agents.workout_agent import create_workout_agent
from agents.fit_agent import create_fit_agent
from core.conversation_manager import (
    create_thread,
    send_user_message,
    run_agent,
    display_agent_responses
)


def create_fitness_system(project, model_name):
    """Initialize the complete fitness advisor multi-agent system."""
    print("\n 🏗️ Building Fitness & Wellness Advisor System...")

    # Create specialized sub-agents
    diet_agent, diet_tool = create_diet_agent(project, model_name)
    workout_agent, workout_tool = create_workout_agent(project, model_name)

    # Create main coordinator agent
    fit_agent = create_fit_agent(project, model_name, diet_tool, workout_tool)

    print("✅ Fitness advisor system ready!")
    return fit_agent, diet_agent, workout_agent


def interactive_session(project, fit_agent):
    """Run an interactive session with the fitness advisor."""
    thread = create_thread(project)

    print("\n🎉 Welcome to your personal Fitness & Wellness Advisor!")
    print("Ask me about nutrition, workouts, meal plans, or your overall wellness goals.")
    print("Type 'quit' to exit.\n")

    while True:
        try:
            user_input = input("👤 You: ").strip()

            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Thanks for using Fitness & Wellness Advisor! Stay healthy!")
                break

            if not user_input:
                continue

            # Send message and get response
            send_user_message(project, thread, user_input)
            run = run_agent(project, thread, fit_agent)
            display_agent_responses(project, thread, run)
            print()  # Add spacing between interactions

        except KeyboardInterrupt:
            print("\n👋 Session ended. Stay fit!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            continue


def demo_session(project, fit_agent):
    """Run a demonstration session with predefined questions."""
    thread = create_thread(project)

    demo_questions = [
        "Hi! I want to lose 10 pounds in a healthy way. Can you help me create a plan?",
        "I'm a beginner and want to start working out at home. What exercises should I do?",
        "Can you suggest a high-protein meal plan for muscle building?",
        "I'm vegan and need workout-friendly meals. Any suggestions?"
    ]

    print("\n🎬 Running Fitness Advisor Demo Session...")
    print("=" * 50)

    for question in demo_questions:
        print(f"\n💭 Demo Question: {question}")
        print("-" * 40)

        send_user_message(project, thread, question)
        run = run_agent(project, thread, fit_agent)
        display_agent_responses(project, thread, run)
        print()


def main():
    """Main application entry point."""
    try:
        setup_logging()
        print("🚀 Starting Fitness & Wellness Advisor...")

        # Initialize Azure connection
        endpoint, model_name = load_configuration()
        project = connect_to_project(endpoint)

        # Create the multi-agent system
        fit_agent, _, _ = create_fitness_system(
            project, model_name)

        # Choose session type
        print("\nSelect session type:")
        print("1. Interactive session (chat with the advisor)")
        print("2. Demo session (see predefined examples)")

        choice = input("Enter choice (1 or 2): ").strip()

        if choice == "1":
            interactive_session(project, fit_agent)
        elif choice == "2":
            demo_session(project, fit_agent)
        else:
            print("Running demo session by default...")
            demo_session(project, fit_agent)

        # Optional cleanup (uncomment if needed)
        # print("\n🧹 Cleaning up agents...")
        # delete_agents(project, fit_agent, diet_agent, workout_agent)

        print("🎉 Fitness & Wellness Advisor session completed!")

    except KeyboardInterrupt:
        print("\n🛑 Program interrupted by user")
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        sys.exit(1)
    finally:
        print("🔴 Program terminated")


if __name__ == "__main__":
    main()
