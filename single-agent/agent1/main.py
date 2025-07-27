import os
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ListSortOrder

print("🚀 Script started...")

# Load environment variables from .env file
print("🔄 Loading environment variables...")
load_dotenv()

# Get environment variables
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
PROJECT_ENDPOINT = os.getenv("PROJECT_ENDPOINT")
MODEL_DEPLOYMENT_NAME = os.getenv("MODEL_DEPLOYMENT_NAME")

# Confirm environment variable values
print(f"🌐 ENVIRONMENT: {ENVIRONMENT}")
if PROJECT_ENDPOINT and MODEL_DEPLOYMENT_NAME:
    print("✅ Found PROJECT_ENDPOINT and MODEL_DEPLOYMENT_NAME")
if not PROJECT_ENDPOINT:
    raise ValueError("❌ PROJECT_ENDPOINT environment variable is not set.")
if not MODEL_DEPLOYMENT_NAME:
    raise ValueError(
        "❌ MODEL_DEPLOYMENT_NAME environment variable is not set.")

# Create AI Project client
print("🔗 Connecting to Azure AI Project...")
project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)

# Set up agent configuration
print("🛠️ Setting up agent configuration...")
agent_name: str = "my-agent-001"
agent_description: str = "A general writing agent"
agent_instructions: str = "You are a helpful writing assistant"

# Create an agent
print("🤖 Creating agent...")
agent = project.agents.create_agent(
    model=MODEL_DEPLOYMENT_NAME,
    name=agent_name,
    instructions=agent_instructions,
    description=agent_description
)
print(f"✅ Agent created: {agent.id}")

# Create a new thread
print("🧵 Creating conversation thread...")
thread = project.agents.threads.create()
print(f"✅ Thread created: {thread.id}")

# Define user message content
user_message_content: str = "Write me a poem about flowers"
print(f"💬 User message: {user_message_content}")

# Send a user message
print("📨 Sending user message to agent...")
message = project.agents.messages.create(
    thread_id=thread.id,
    role="user",
    content=user_message_content
)
print(f"✅ Message sent: {message.id}")

# Run the agent
print("🏃 Running agent...")
run = project.agents.runs.create_and_process(
    thread_id=thread.id,
    agent_id=agent.id
)

if run.status == "failed":
    print(f"❌ Run failed: {run.last_error}")
else:
    print(f"✅ Run completed with status: {run.status}")

# Retrieve and display agent's response
print("📥 Fetching messages from thread...")
messages = project.agents.messages.list(
    thread_id=thread.id, order=ListSortOrder.ASCENDING
)

for message in messages:
    if message.run_id == run.id and message.text_messages:
        print(
            f"\n🧠 {message.role.capitalize()}: {message.text_messages[-1].text.value}")

# Optionally delete the agent
# print("🗑️ Deleting agent...")
# project.agents.delete_agent(agent.id)
# print("✅ Agent deleted")

print("🎉 Script completed successfully.")
