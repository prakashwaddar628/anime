import requests
import time
from typing import Optional

# The base URL for the Jikan API v4
JIKAN_API_BASE_URL = "https://api.jikan.moe/v4"

def get_character_image_url(character_name: str) -> Optional[str]:
    """
    Fetches the primary image URL for a given character from the Jikan API.

    Args:
        character_name: The name of the anime character to search for.

    Returns:
        The image URL as a string, or None if not found or an error occurs.
    """
    if not character_name:
        return None

    # Construct the API request URL
    # We use q={character_name} to search and limit=1 to get the most relevant result.
    request_url = f"{JIKAN_API_BASE_URL}/characters?q={character_name}&limit=1"
    
    try:
        # Make the API call
        response = requests.get(request_url)
        response.raise_for_status()  # Raises an exception for bad status codes (4xx or 5xx)
        
        data = response.json()
        
        # Check if the 'data' array is not empty and has results
        if data.get("data"):
            # Extract the JPG image URL from the nested structure
            image_url = data["data"][0].get("images", {}).get("jpg", {}).get("image_url")
            return image_url
        else:
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error calling Jikan API for '{character_name}': {e}")
        return None
    except (KeyError, IndexError) as e:
        print(f"Error parsing Jikan API response for '{character_name}': {e}")
        return None
    finally:
        # IMPORTANT: Add a small delay to respect the API's rate limits
        # Jikan's public API recommends 1 request per second.
        time.sleep(1)