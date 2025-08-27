import requests
import os
from dotenv import load_dotenv

# --- IMPORTANT ---
# This script MUST be in the same directory as your .env file to work.

def run_test():
    """
    A simple, isolated test to check the MAL API call.
    """
    print("--- Starting MAL API Test ---")

    # Load environment variables from the .env file
    load_dotenv()
    
    # Get the Client ID from the environment
    client_id = os.getenv("MAL_CLIENT_ID")

    if not client_id:
        print("!!! ERROR: MAL_CLIENT_ID not found in .env file. Please check the file.")
        return

    print(f"Found Client ID: '{client_id}'")
    
    # 1. Let's hardcode a famous character to remove variables
    character_name = "Lelouch Lamperouge"
    
    # 2. Define the exact URL and headers
    request_url = f"https://api.myanimelist.net/v2/characters?q={character_name}&limit=1"
    headers = {
        "X-MAL-CLIENT-ID": client_id
    }

    print(f"Requesting URL: {request_url}")
    print(f"Using Headers: {headers}")

    try:
        # 3. Make the request
        response = requests.get(request_url, headers=headers)

        # 4. Print the raw results
        print("\n--- RESULTS ---")
        print(f"Status Code: {response.status_code}")
        print("Response Headers:")
        # Print response headers to see if there are any clues
        for key, value in response.headers.items():
            print(f"  {key}: {value}")
        
        print("\nResponse Body (Text):")
        print(response.text)

        # This will raise an error if the status code is 4xx or 5xx
        response.raise_for_status()
        
        print("\n--- SUCCESS ---")
        print("The API call was successful and returned a 2xx status code.")
        print("The Client ID is working correctly.")

    except requests.exceptions.HTTPError as e:
        print("\n--- FAILURE ---")
        print(f"The API call failed with an HTTP Error: {e}")
        print("This confirms the 404 error is coming directly from the API.")
        print("This strongly suggests the Client ID is invalid, disabled, or incorrect.")

    except Exception as e:
        print(f"\n--- An Unexpected Error Occurred ---")
        print(e)


if __name__ == "__main__":
    run_test()