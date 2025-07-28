import logging
from azure.ai.agents.models import ConnectedAgentTool


def create_diet_agent(project, model_name):
    """Create the DietAgent specialized for meal planning and nutrition advice."""
    agent_name = "diet_agent"
    agent_description = "Specialized nutrition and meal planning expert"
    agent_instructions = """
    You are DietAgent, a specialized nutrition and meal planning expert. Your responsibilities include:
    
    🥗 NUTRITION EXPERTISE:
    - Create personalized meal plans based on dietary preferences and restrictions
    - Provide calorie breakdowns and macro-nutrient information
    - Generate shopping lists for meal plans
    - Offer healthy recipe suggestions and meal prep tips
    
    🎯 DIETARY SPECIALIZATIONS:
    - Vegan and vegetarian meal planning
    - Keto and low-carb diets
    - Intermittent fasting schedules
    - Mediterranean and DASH diets
    - Allergy-friendly meal options (gluten-free, dairy-free, etc.)
    
    📊 CURRENT NUTRITION DATABASE:
    - High-protein foods: Chicken breast (165 cal/100g), Salmon (206 cal/100g), Lentils (116 cal/100g)
    - Complex carbs: Quinoa (120 cal/100g), Sweet potato (86 cal/100g), Oats (68 cal/100g)
    - Healthy fats: Avocado (160 cal/100g), Almonds (576 cal/100g), Olive oil (884 cal/100ml)
    - Vegetables: Spinach (23 cal/100g), Broccoli (34 cal/100g), Bell peppers (31 cal/100g)
    
    Always provide practical, evidence-based nutrition advice and create realistic meal plans that fit the user's lifestyle and goals.
    """

    logging.info(f"🥗 Creating diet agent ({agent_name})...")

    try:
        agent = project.agents.create_agent(
            model=model_name,
            name=agent_name,
            description=agent_description,
            instructions=agent_instructions,
        )

        logging.info(f"✅ {agent_name} created: {agent.id}")

        connected_tool = ConnectedAgentTool(
            id=agent.id,
            name=agent_name,
            description="Provides personalized nutrition advice, meal plans, and dietary guidance"
        )

        logging.info(f"✅ {agent_name} connected to tools.")
        return agent, connected_tool

    except Exception as e:
        logging.error(f"❌ Failed to create diet agent ({agent_name}): {e}")
        raise
