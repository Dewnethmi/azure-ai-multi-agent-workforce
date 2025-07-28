import time
import logging
from azure.ai.agents.models import MessageRole, ListSortOrder


def create_thread(project):
    """Create a conversation thread for the fitness advisor session."""
    # logging.info("🧵 Creating conversation thread...")
    print("\n🧵 Creating conversation thread...")

    try:
        thread = project.agents.threads.create()
        # logging.info(f"✅ Thread created: {thread.id}")
        print(f"✅ Thread created: {thread.id}")
        return thread

    except Exception as e:
        # logging.error(f"❌ Failed to create conversation thread: {e}")
        print(f"❌ Failed to create conversation thread: {e}")
        raise


def send_user_message(project, thread, content):
    """Send a user message to the conversation thread."""
    # logging.info(f"💬 User message: {content}")
    print(f"\n💬 User message: {content}")
    # logging.info("📨 Sending user message to fitness advisor...")
    print("📨 Sending user message to fitness advisor...")

    try:
        message = project.agents.messages.create(
            thread_id=thread.id,
            role=MessageRole.USER,
            content=content
        )
        # logging.info(f"✅ Message sent: {message.id}")
        print(f"✅ Message sent: {message.id}")
        return message

    except Exception as e:
        # logging.error(f"❌ Failed to send user message: {e}")
        print(f"❌ Failed to send user message: {e}")
        raise


def run_agent(project, thread, agent, poll_interval=2, timeout=60):
    """Execute the agent run and poll for completion."""
    # logging.info("🏃 Starting fitness advisor run...")
    print("🏃 Starting fitness advisor run...")

    try:
        run = project.agents.runs.create(
            thread_id=thread.id,
            agent_id=agent.id
        )
        # logging.info(f"🔄 Run initiated: {run.id} — Status: {run.status}")
        print(f"🔄 Run initiated: {run.id} — Status: {run.status}")

        # Poll for completion
        start_time = time.time()
        while run.status in ["queued", "in_progress"]:
            if time.time() - start_time > timeout:
                raise TimeoutError(
                    "⏰ Run timed out while waiting for completion.")

            time.sleep(poll_interval)
            run = project.agents.runs.get(thread_id=thread.id, run_id=run.id)
            # logging.info(f"📡 Run status: {run.status}")
            print(f"📡 Run status: {run.status}")

        # Final status
        if run.status == "failed":
            # logging.error(f"❌ Run failed: {run.last_error}")
            print(f"❌ Run failed: {run.last_error}")
        else:
            # logging.info(f"✅ Run completed with status: {run.status}")
            print(f"✅ Run completed with status: {run.status}")

        return run

    except Exception as e:
        # logging.error(f"💥 Failed to run fitness advisor: {e}", exc_info=True)
        print(f"💥 Failed to run fitness advisor: {e}")
        raise


def display_agent_responses(project, thread, run):
    """Fetch and display agent responses from the conversation thread."""
    # logging.info("📥 Fetching messages from thread...")
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
                    # logging.info(
                    #     f"\n🧠 {msg.role.capitalize()}: {last_message}")
                    print(f"\n🧠 {msg.role.capitalize()}: {last_message}")
                except (IndexError, AttributeError) as inner_e:
                    # logging.warning(
                    #     f"⚠️ Skipped a malformed message: {inner_e}")
                    print(f"⚠️ Skipped a malformed message: {inner_e}")

    except Exception as e:
        # logging.error(f"❌ Failed to fetch/display agent responses: {e}")
        print(f"❌ Failed to fetch/display agent responses: {e}")
        raise
