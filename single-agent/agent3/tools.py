import os
import json
import requests

# ---------------------------------------------
# Inventory API Tools
# ---------------------------------------------
INVENTORY_API_URI = os.getenv(
    "INVENTORY_API_URI", "https://simple-fastapi-inventory.azurewebsites.net/")

# Timeout for API requests in seconds
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 10))

# Optional: Project/Agent environment variables
PROJECT_ENDPOINT = os.getenv("PROJECT_ENDPOINT")
MODEL_DEPLOYMENT_NAME = os.getenv("MODEL_DEPLOYMENT_NAME")
AGENT_ID = os.getenv("AGENT_ID")
THREAD_ID = os.getenv("THREAD_ID")


def get_inventory_details() -> str:
    """
    Fetch all inventory items from the API.

    Returns a JSON string of all items.
    """
    url = f"{INVENTORY_API_URI}/items"
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        return json.dumps({"error": str(e)})


def get_inventory_item(
    item_id
) -> str:
    """
    Fetch a single inventory item by ID.

    :param item_id: ID of the inventory item.
    :return: JSON string of the item details.
    """
    url = f"{INVENTORY_API_URI}/items/{item_id}"
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        return json.dumps({"error": str(e)})


def create_inventory_item(
    name,
    price,
    quantity,
    description=None
) -> str:
    """
    Create a new inventory item.

    :param name: Name of the item.
    :param price: Price of the item.
    :param quantity: Quantity available.
    :param description: Optional description.
    :return: JSON string of the created item.
    """
    url = f"{INVENTORY_API_URI}/items/"
    payload = {
        "name": name,
        "price": price,
        "quantity": quantity,
    }
    if description is not None:
        payload["description"] = description

    try:
        response = requests.post(url, json=payload, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        return json.dumps({"error": str(e)})


def update_inventory_item(
    item_id,
    name=None,
    price=None,
    quantity=None,
    description=None
) -> str:
    url = f"{INVENTORY_API_URI}/items/{item_id}"
    payload = {k: v for k, v in {
        "name": name,
        "price": price,
        "quantity": quantity,
        "description": description
    }.items() if v is not None}

    try:
        response = requests.put(url, json=payload, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        return json.dumps({"error": str(e)})


def delete_inventory_item(
    item_id
) -> str:
    """
    Delete an inventory item.

    :param item_id: ID of the item to delete.
    :return: JSON string with result of the operation.
    """
    url = f"{INVENTORY_API_URI}/items/{item_id}"
    try:
        response = requests.delete(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.text if response.text else json.dumps({"success": True})
    except requests.RequestException as e:
        return json.dumps({"error": str(e)})
