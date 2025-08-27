import os
import json

def create_class_mapping(dataset_path: str, output_file: str):
    """
    Scans a dataset directory, finds all class folders, sorts them alphabetically,
    and creates a JSON file mapping the index to the class name.
    """
    print(f"Scanning dataset directory: {dataset_path}")
    
    # Get all the subdirectories (which are our character names)
    try:
        class_names = [d for d in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, d))]
    except FileNotFoundError:
        print(f"Error: The directory '{dataset_path}' was not found.")
        return

    if not class_names:
        print("Error: No character folders found in the dataset directory.")
        return

    # Sort them alphabetically - this is the crucial step that matches PyTorch's ImageFolder
    class_names.sort()
    
    print(f"Found {len(class_names)} classes. The first few are: {class_names[:5]}")
    
    # Create the dictionary mapping index (as a string) to class name
    class_to_idx = {str(i): name for i, name in enumerate(class_names)}
    
    # Write the dictionary to the specified output file
    try:
        with open(output_file, 'w') as f:
            json.dump(class_to_idx, f, indent=2)
        print(f"Successfully created '{output_file}'!")
        print("This file is now ready to be used with your FastAPI application.")
    except IOError as e:
        print(f"Error writing to file '{output_file}': {e}")


if __name__ == '__main__':
    # --- CONFIGURE THIS ---
    # IMPORTANT: Change this path to point to the location of your
    # final training dataset folder.
    DATASET_DIRECTORY = './dataset'

    # This is the output file our FastAPI app uses.
    OUTPUT_JSON_FILE = 'class_names.json' 
    
    create_class_mapping(DATASET_DIRECTORY, OUTPUT_JSON_FILE)