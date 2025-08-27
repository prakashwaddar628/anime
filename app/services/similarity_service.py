import json
from scipy.stats import wasserstein_distance
from typing import List, Dict

def _load_character_database() -> List[Dict]:
    """Loads the character data from the mock JSON database."""
    try:
        with open("mock_character_db.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Warning: mock_character_db.json not found.")
        return []
    except json.JSONDecodeError:
        print("Warning: Could not decode mock_character_db.json.")
        return []

def _create_tag_vocabulary(database: List[Dict]) -> List[str]:
    """Creates a sorted list of all unique tags from the database."""
    all_tags = set()
    for character in database:
        for tag in character.get("tags", []):
            all_tags.add(tag)
    return sorted(list(all_tags))

def _vectorize_tags(tags: List[str], vocabulary: List[str]) -> List[int]:
    """Converts a list of tags into a numerical vector based on the vocabulary."""
    vector = [0] * len(vocabulary)
    for tag in tags:
        if tag in vocabulary:
            index = vocabulary.index(tag)
            vector[index] = 1 # Mark the presence of the tag
    return vector

def find_similar_characters(
    predicted_character_name: str,
    predicted_character_tags: List[str],
    top_n: int = 3
) -> List[Dict]:
    """
    Finds the most similar characters based on Wasserstein distance of their tags.

    Args:
        predicted_character_name: The name of the character we are comparing against.
        predicted_character_tags: The tags of the character.
        top_n: The number of similar characters to return.

    Returns:
        A list of the top N most similar characters.
    """
    character_db = _load_character_database()
    if not character_db:
        return []

    # Create a vocabulary of all possible tags from our database
    vocabulary = _create_tag_vocabulary(character_db)
    
    # Convert the predicted character's tags into a numerical vector
    predicted_vector = _vectorize_tags(predicted_character_tags, vocabulary)

    distances = []
    for db_character in character_db:
        # Don't compare a character with itself
        if db_character["name"] == predicted_character_name:
            continue
        
        # Convert each DB character's tags into a vector
        db_vector = _vectorize_tags(db_character.get("tags", []), vocabulary)
        
        # Calculate the Wasserstein distance between the two vectors
        distance = wasserstein_distance(predicted_vector, db_vector)
        distances.append({"name": db_character["name"], "anime": db_character["anime"], "distance": distance})
    
    # Sort the characters by their distance (smallest distance is most similar)
    sorted_characters = sorted(distances, key=lambda x: x["distance"])
    
    # Return the top N results
    return sorted_characters[:top_n]