# core/conversation_manager.py

import time
from azure.ai.agents.models import MessageRole, ListSortOrder


def create_thread(project):
    """
    Create a conversation thread for the inventory management session.

    Args:
        project: Azure AI Project client

    Returns:
        thread: Created conversation thread

    Raises:
        Exception: If thread creation fails
    """
    print("\n🧵 Creating conversation thread...")

    try:
        thread = project.agents.threads.create()
        print(f"✅ Thread created: {thread.id}")
        return thread

    except Exception as e:
        print(f"❌ Failed to create conversation thread: {e}")
        raise


def send_user_message(project, thread, content):
    """
    Send a user message to the conversation thread.

    Args:
        project: Azure AI Project client
        thread: Conversation thread object
        content: Message content to send

    Returns:
        message: Created message object

    Raises:
        Exception: If message sending fails
    """
    print(f"\n💬 User message: {content}")
    print("📨 Sending message to store manager...")

    try:
        if not content or not content.strip():
            raise ValueError("Message content cannot be empty")

        message = project.agents.messages.create(
            thread_id=thread.id,
            role=MessageRole.USER,
            content=content
        )
        print(f"✅ Message sent: {message.id}")
        return message

    except Exception as e:
        print(f"❌ Failed to send user message: {e}")
        raise


def run_agent(project, thread, agent, poll_interval=2, timeout=60):
    """
    Run the AI agent on a conversation thread and poll until completion.

    Args:
        project: Azure AI Project client
        thread: Conversation thread object
        agent: AI agent to run
        poll_interval (int, optional): Seconds to wait between status checks. Defaults to 2.
        timeout (int, optional): Max time (in seconds) to wait for run to complete. Defaults to 60.

    Returns:
        run: Run object containing final status and metadata

    Raises:
        TimeoutError: If the agent run does not complete within the timeout period
        Exception: If run initiation or polling fails
    """
    print("🏃 Starting fitness advisor run...")

    try:
        run = project.agents.runs.create(
            thread_id=thread.id,
            agent_id=agent.id
        )
        print(f"🔄 Run initiated: {run.id} — Status: {run.status}")

        start_time = time.time()
        while run.status in ["queued", "in_progress"]:
            if time.time() - start_time > timeout:
                raise TimeoutError(
                    "⏰ Run timed out while waiting for completion.")

            time.sleep(poll_interval)
            run = project.agents.runs.get(thread_id=thread.id, run_id=run.id)
            print(f"📡 Run status: {run.status}")

        if run.status == "failed":
            print(f"❌ Run failed: {run.last_error}")
        else:
            print(f"✅ Run completed with status: {run.status}")

        return run

    except Exception as e:
        print(f"💥 Failed to run fitness advisor: {e}")
        raise


def display_agent_responses(project, thread, run):
    """
    Fetch and display the agent's responses related to a specific run.

    Args:
        project: Azure AI Project client
        thread: Conversation thread object
        run: Run object that triggered the agent response

    Returns:
        None

    Raises:
        Exception: If fetching or displaying messages fails
    """
    print("📥 Fetching messages from thread...")

    try:
        messages = project.agents.messages.list(
            thread_id=thread.id,
            order=ListSortOrder.ASCENDING
        )

        for msg in messages:
            if msg.run_id == run.id and msg.text_messages:
                try:
                    last_message = msg.text_messages[-1].text.value
                    print(f"\n🧠 {msg.role.capitalize()}: {last_message}")
                except (IndexError, AttributeError) as inner_e:
                    print(f"⚠️ Skipped a malformed message: {inner_e}")

    except Exception as e:
        print(f"❌ Failed to fetch/display agent responses: {e}")
        raise
