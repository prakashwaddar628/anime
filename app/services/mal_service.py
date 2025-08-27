import requests
from typing import Optional
from ..core.config import settings # Import our settings to get the Client ID

# The base URL for the official MAL API v2
API_BASE_URL = "https://api.myanimelist.net/v2"

def get_character_image_url(character_name: str) -> Optional[str]:
    """
    Fetches the primary image URL for a given character from the official MAL API
    using a direct HTTP request with the Client ID.

    Args:
        character_name: The name of the anime character to search for.

    Returns:
        The image URL as a string, or None if not found or an error occurs.
    """
    if not character_name or not settings.MAL_CLIENT_ID:
        return None

    # For public data access, the Client ID is sent as a header
    headers = {
        "X-MAL-CLIENT-ID": settings.MAL_CLIENT_ID
    }
    
    # Construct the API request URL for character search
    # We search for the name and limit the result to 1 to get the most relevant match.
    request_url = f"{API_BASE_URL}/characters?q={character_name}&limit=1"
    
    try:
        # Make the API call
        response = requests.get(request_url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        
        data = response.json()
        
        # The response structure is {'data': [{'node': {...}}]}
        if data.get("data"):
            # The character information is inside the 'node' key
            character_node = data["data"][0].get("node")
            if character_node:
                # The image URL is in the 'main_picture' dictionary
                main_picture = character_node.get("main_picture")
                if main_picture:
                    # 'large' is usually better quality than 'medium'
                    return main_picture.get("large") or main_picture.get("medium")
        
        return None # Return None if no character data was found

    except requests.exceptions.RequestException as e:
        print(f"Error calling MAL API for '{character_name}': {e}")
        return None
    except (KeyError, IndexError, TypeError) as e:
        print(f"Error parsing MAL API response for '{character_name}': {e}")
        return None