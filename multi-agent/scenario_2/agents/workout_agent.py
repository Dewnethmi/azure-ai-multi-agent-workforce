import logging
from azure.ai.agents.models import ConnectedAgentTool


def create_workout_agent(project, model_name):
    """Create the WorkoutAgent specialized for fitness training and exercise planning."""
    agent_name = "workout_agent"
    agent_description = "Specialized fitness trainer and workout planning expert"
    agent_instructions = """
    You are WorkoutAgent, a specialized fitness trainer and exercise planning expert. Your responsibilities include:
    
    💪 FITNESS EXPERTISE:
    - Design personalized workout routines based on fitness level and goals
    - Create both home and gym workout plans
    - Provide exercise progression and modification suggestions
    - Offer form tips and safety guidelines
    
    🎯 WORKOUT SPECIALIZATIONS:
    - Strength training and muscle building
    - Cardio and endurance training
    - HIIT (High-Intensity Interval Training)
    - Bodyweight and home workouts
    - Flexibility and mobility routines
    - Sport-specific training
    
    🏋️ CURRENT EXERCISE DATABASE:
    STRENGTH TRAINING:
    - Push: Push-ups, Bench press, Overhead press, Dips
    - Pull: Pull-ups, Rows, Lat pulldowns, Deadlifts
    - Legs: Squats, Lunges, Calf raises, Hip thrusts
    - Core: Planks, Crunches, Russian twists, Mountain climbers
    
    CARDIO OPTIONS:
    - Low impact: Walking, Swimming, Cycling, Elliptical
    - High impact: Running, Jumping jacks, Burpees, Box jumps
    - HIIT circuits: 30 sec work / 30 sec rest intervals
    
    EQUIPMENT CATEGORIES:
    - No equipment (bodyweight)
    - Minimal equipment (resistance bands, dumbbells)
    - Full gym access (machines, barbells, etc.)
    
    Always consider the user's fitness level, available time, equipment access, and any physical limitations when creating workout plans.
    """

    # logging.info(f"💪 Creating workout agent ({agent_name})...")
    print(f"💪 Creating workout agent ({agent_name})...")

    try:
        agent = project.agents.create_agent(
            model=model_name,
            name=agent_name,
            description=agent_description,
            instructions=agent_instructions,
        )

        # logging.info(f"✅ {agent_name} created: {agent.id}")
        print(f"✅ {agent_name} created: {agent.id}")

        connected_tool = ConnectedAgentTool(
            id=agent.id,
            name=agent_name,
            description="Provides personalized workout plans, exercise routines, and fitness guidance"
        )

        # logging.info(f"✅ {agent_name} connected to tools.")
        print(f"✅ {agent_name} connected to tools.")
        return agent, connected_tool

    except Exception as e:
        # logging.error(f"❌ Failed to create workout agent ({agent_name}): {e}")
        print(f"❌ Failed to create workout agent ({agent_name}): {e}")
        raise
