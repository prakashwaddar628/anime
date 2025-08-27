import json
from typing import List, Dict, Set

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

def _calculate_jaccard_distance(set_a: Set[str], set_b: Set[str]) -> float:
    """Calculates the Jaccard distance between two sets of tags."""
    intersection = len(set_a.intersection(set_b))
    union = len(set_a.union(set_b))
    if union == 0:
        return 0.0
    distance = 1.0 - (intersection / union)
    return distance

def find_similar_characters(
    predicted_character_name: str,
    predicted_character_tags: List[str],
    top_n: int = 3
) -> List[Dict]:
    """
    Finds the most similar characters based on Jaccard distance of their tags.
    """
    # --- START OF DEBUGGING ---
    print("\n" + "="*50)
    print("--- Running Similarity Service ---")
    print(f"Searching for characters similar to: '{predicted_character_name}'")
    print(f"With tags: {predicted_character_tags}")
    print("="*50 + "\n")
    # --- END OF DEBUGGING ---

    character_db = _load_character_database()
    if not character_db:
        print("!!! DEBUG: Character database is empty or could not be loaded.")
        return []

    print(f"--- DEBUG: Loaded {len(character_db)} characters from the database.")
    
    predicted_tags_set = set(predicted_character_tags)
    
    distances = []
    print("\n--- DEBUG: Calculating distances for each character ---")
    for db_character in character_db:
        # Don't compare a character with itself
        if db_character["name"].lower() == predicted_character_name.lower():
            print(f"Skipping '{db_character['name']}' (self-comparison).")
            continue
        
        db_tags_set = set(db_character.get("tags", []))
        distance = _calculate_jaccard_distance(predicted_tags_set, db_tags_set)
        
        # --- DEBUG PRINT INSIDE LOOP ---
        print(f"  - Compared with: '{db_character['name']}'")
        print(f"    DB Tags: {list(db_tags_set)}")
        print(f"    Common Tags: {list(predicted_tags_set.intersection(db_tags_set))}")
        print(f"    Calculated Distance: {distance:.4f}")
        # --- END DEBUG PRINT ---

        distances.append({
            "name": db_character["name"], 
            "anime": db_character["anime"], 
            "distance": distance
        })
    
    print("\n--- DEBUG: List of all calculated distances (unsorted) ---")
    print(distances)

    # Sort the characters by their distance (smallest distance is most similar)
    sorted_characters = sorted(distances, key=lambda x: x["distance"])
    
    print("\n--- DEBUG: List of distances (SORTED) ---")
    print(sorted_characters)

    final_results = sorted_characters[:top_n]

    print("\n--- DEBUG: Final Top 3 Results ---")
    print(final_results)
    print("="*50 + "\n")

    return final_results