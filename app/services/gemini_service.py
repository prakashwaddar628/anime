import google.generativeai as genai
import json
from ..core.config import settings # Import our settings

# Configure the generative AI client with the API key
genai.configure(api_key=settings.GOOGLE_API_KEY)

# Initialize the generative model
model = genai.GenerativeModel('gemini-2.5-flash')

def get_character_details_from_gemini(character_name: str) -> dict:
    """
    Sends a character name to the Gemini API and gets structured details.
    
    Args:
        character_name: The name of the anime character.
        
    Returns:
        A dictionary containing the character's details or an error message.
    """
    if not character_name:
        return {"error": "Character name is empty."}
    
    # This is our prompt. We instruct the model to return a JSON object
    # with a specific structure. This makes the output predictable and easy to parse.
    prompt = f"""
    Please provide details for the anime character named "{character_name}".
    I need the response in a specific JSON format. The JSON object should have the following keys:
    - "name": The character's full, corrected name.
    - "about": A 2-3 sentence summary about the character.
    - "tags": A JSON array of 5-7 descriptive tags about the character's physical appearance and style (e.g., "long pink hair", "blue eyes", "wears glasses", "school uniform").
    - "anime_name": The full name of the primary anime the character is in.
    - "streaming_platforms": A JSON array of well-known, legal websites where the anime can be watched (e.g., "Crunchyroll", "Netflix", "Hulu"). If none, provide an empty array.

    Here is an example for "Anya Forger":
    {{
        "name": "Anya Forger",
        "about": "Anya Forger is a young girl with telepathic abilities who was adopted by the spy Loid Forger for his mission. She is curious, cheerful, and often misinterprets situations, leading to comedic outcomes.",
        "tags": ["short pink hair", "green eyes", "child", "school uniform", "black hair accessories"],
        "anime_name": "Spy x Family",
        "streaming_platforms": ["Crunchyroll", "Hulu", "Netflix"]
    }}

    Now, generate the JSON for "{character_name}":
    """
    
    try:
        # Send the prompt to the model
        response = model.generate_content(prompt)
        
        # The response text might have markdown formatting (```json ... ```)
        # We need to clean it to get the raw JSON string.
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "").strip()
        
        # Parse the cleaned string into a Python dictionary
        character_details = json.loads(cleaned_response)
        
        return character_details

    except json.JSONDecodeError:
        return {"error": "Failed to parse JSON response from Gemini."}
    except Exception as e:
        return {"error": f"An unexpected error occurred with the Gemini API: {str(e)}"}