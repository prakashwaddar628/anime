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
    """
    if not character_name:
        return {"error": "Character name is empty."}
    
    # --- PROMPT HAS BEEN UPDATED ---
    # We are now much more specific about the URL format.
    prompt = f"""
    Please provide details for the anime character named "{character_name}".
    I need the response in a specific JSON format. The JSON object should have the following keys:
    - "name": The character's full, corrected name.
    - "about": A 2-3 sentence summary about the character.
    - "tags": A JSON array of 5-7 descriptive tags about the character's physical appearance and style.
    - "anime_name": The full name of the primary anime the character is in.
    - "streaming_platforms": A JSON array of objects. Each object must have "name" and "url" keys.
      IMPORTANT: The "url" should be the simplest, cleanest version possible.
      For example, prefer 'https://www.crunchyroll.com/naruto' over 'https://www.crunchyroll.com/series/GY9PJ5KWR/naruto' and 'https://www.hulu.com/naruto over 'www.hulu.com/series/naruto'.
      Avoid long, random-looking series IDs in the URL if a cleaner one exists.

    Here is an example for "Anya Forger" with the desired URL format:
    {{
        "name": "Anya Forger",
        "about": "Anya Forger is a young girl with telepathic abilities who was adopted by the spy Loid Forger for his mission. She is curious, cheerful, and often misinterprets situations, leading to comedic outcomes.",
        "tags": ["short pink hair", "green eyes", "child", "school uniform", "black hair accessories"],
        "anime_name": "Spy x Family",
        "streaming_platforms": [
            {{"name": "Crunchyroll", "url": "https://www.crunchyroll.com/spy-x-family"}},
            {{"name": "Hulu", "url": "https://www.hulu.com/spy-x-family"}}
        ]
    }}

    Now, generate the JSON for "{character_name}":
    """
    
    try:
        response = model.generate_content(prompt)
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "").strip()
        character_details = json.loads(cleaned_response)
        return character_details

    except json.JSONDecodeError:
        return {"error": "Failed to parse JSON response from Gemini."}
    except Exception as e:
        return {"error": f"An unexpected error occurred with the Gemini API: {str(e)}"}