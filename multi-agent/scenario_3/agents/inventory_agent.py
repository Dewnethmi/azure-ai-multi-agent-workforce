# agents/inventory_agent.py

from azure.ai.agents.models import ConnectedAgentTool, OpenApiTool, OpenApiAnonymousAuthDetails

SERVER = "https://simple-fastapi-inventory.azurewebsites.net"
APPLICATION_JSON = "application/json"
ITEM_SCHEMA_REF = "#/components/schemas/Item"

openapi_spec = {
    "openapi": "3.1.0",
    "info": {"title": "Inventory API", "version": "0.1.0"},
    "servers": [{"url": SERVER}],
    "paths": {
        "/items/": {
            "get": {
                "operationId": "list_items_items__get",
                "responses": {
                    "200": {
                        "content": {
                            APPLICATION_JSON: {
                                "schema": {
                                    "type": "array",
                                    "items": {"$ref": ITEM_SCHEMA_REF}
                                }
                            }
                        }
                    }
                }
            },
            "post": {
                "operationId": "create_item_items__post",
                "requestBody": {
                    "content": {
                        APPLICATION_JSON: {
                            "schema": {"$ref": "#/components/schemas/ItemCreate"}
                        }
                    }
                },
                "responses": {
                    "201": {
                        "content": {
                            APPLICATION_JSON: {
                                "schema": {"$ref": ITEM_SCHEMA_REF}
                            }
                        }
                    }
                }
            }
        },
        "/items/{item_id}": {
            "get": {
                "operationId": "get_item_items__item_id__get",
                "parameters": [
                    {
                        "name": "item_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"}
                    }
                ],
                "responses": {
                    "200": {
                        "content": {
                            APPLICATION_JSON: {
                                "schema": {"$ref": ITEM_SCHEMA_REF}
                            }
                        }
                    }
                }
            },
            "put": {
                "operationId": "update_item_items__item_id__put",
                "parameters": [
                    {
                        "name": "item_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"}
                    }
                ],
                "requestBody": {
                    "content": {
                        APPLICATION_JSON: {
                            "schema": {"$ref": "#/components/schemas/ItemUpdate"}
                        }
                    }
                },
                "responses": {
                    "200": {
                        "content": {
                            APPLICATION_JSON: {
                                "schema": {"$ref": ITEM_SCHEMA_REF}
                            }
                        }
                    }
                }
            },
            "delete": {
                "operationId": "delete_item_items__item_id__delete",
                "parameters": [
                    {
                        "name": "item_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"}
                    }
                ],
                "responses": {
                    "200": {"description": "Deleted"}
                }
            }
        }
    },
    "components": {
        "schemas": {
            "Item": {
                "type": "object",
                "required": ["id", "name", "price", "quantity"],
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "description": {"anyOf": [{"type": "string"}, {"type": "null"}]},
                    "price": {"type": "number"},
                    "quantity": {"type": "integer"}
                }
            },
            "ItemCreate": {
                "type": "object",
                "required": ["name", "price", "quantity"],
                "properties": {
                    "name": {"type": "string"},
                    "description": {"anyOf": [{"type": "string"}, {"type": "null"}]},
                    "price": {"type": "number"},
                    "quantity": {"type": "integer"}
                }
            },
            "ItemUpdate": {
                "type": "object",
                "properties": {
                    "name": {"anyOf": [{"type": "string"}, {"type": "null"}]},
                    "description": {"anyOf": [{"type": "string"}, {"type": "null"}]},
                    "price": {"anyOf": [{"type": "number"}, {"type": "null"}]},
                    "quantity": {"anyOf": [{"type": "integer"}, {"type": "null"}]}
                }
            }
        }
    }
}

auth = OpenApiAnonymousAuthDetails()

tool = OpenApiTool(
    name="inventory_api",
    spec=openapi_spec,
    description="Inventory management via REST API - supports full CRUD operations",
    auth=auth
)


def create_inventory_agent(project, model_name):
    """
    Create an inventory management agent with OpenAPI function calling capabilities.

    Args:
        project: Azure AI Project client
        model_name: Name of the model deployment to use

    Returns:
        tuple: (agent, connected_tool) - The created agent and its connected tool

    Raises:
        Exception: If agent creation fails
    """
    agent_name = "inventory_agent"
    agent_description = "Manages inventory operations using OpenAPI function calls"
    agent_instructions = (
        "You are an Inventory Management Agent. Use the available functions to:\n"
        "- List all items in inventory\n"
        "- Get specific item details by ID\n"
        "- Create new inventory items\n"
        "- Update existing items (name, description, price, quantity)\n"
        "- Delete items from inventory\n"
        "Always provide clear, accurate information about inventory status and operations."
    )

    print(f"🤖 Creating ({agent_name})...")

    try:
        agent = project.agents.create_agent(
            model=model_name,
            name=agent_name,
            description=agent_description,
            instructions=agent_instructions,
            tools=tool.definitions
        )

        print(f"✅ {agent_name} created: {agent.id}")

        connected_tool = ConnectedAgentTool(
            id=agent.id,
            name=agent_name,
            description="Inventory management with full CRUD operations via REST API"
        )

        print(f"✅ {agent_name} connected to tools.")
        return agent, connected_tool

    except Exception as e:
        print(f"❌ Failed to create agent ({agent_name}): {e}")
        raise
