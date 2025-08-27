import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import timm
from tqdm import tqdm
import shutil
import random

# --- 1. CONFIGURATION ---
# IMPORTANT: Adjust these paths and parameters for your setup.

# Path to your full, unsplit dataset
SOURCE_DATASET_PATH = './dataset' 

# Path where the script will create 'train' and 'val' subfolders
PROCESSED_DATASET_PATH = './processed_dataset' 

# Model Configuration
MODEL_NAME = 'efficientnet_b0'
NUM_EPOCHS = 10  # Start with 10-15 and increase if needed
BATCH_SIZE = 32  # Adjust based on your GPU memory (16, 32, 64)
LEARNING_RATE = 0.001
VALIDATION_SPLIT = 0.2 # Use 20% of the data for validation

# Output file for the trained model
OUTPUT_MODEL_FILE = 'anime_character_model.pth'

# --- 2. DATA PREPARATION ---

def split_dataset(source_path, processed_path, split_ratio):
    """Splits the dataset into training and validation sets."""
    if os.path.exists(processed_path):
        print(f"'{processed_path}' already exists. Skipping split.")
        return
    
    print(f"Creating train/val split in '{processed_path}'...")
    os.makedirs(os.path.join(processed_path, 'train'), exist_ok=True)
    os.makedirs(os.path.join(processed_path, 'val'), exist_ok=True)

    for class_name in os.listdir(source_path):
        class_path = os.path.join(source_path, class_name)
        if not os.path.isdir(class_path):
            continue

        os.makedirs(os.path.join(processed_path, 'train', class_name), exist_ok=True)
        os.makedirs(os.path.join(processed_path, 'val', class_name), exist_ok=True)

        files = [f for f in os.listdir(class_path) if os.path.isfile(os.path.join(class_path, f))]
        random.shuffle(files)
        
        split_index = int(len(files) * (1 - split_ratio))
        train_files = files[:split_index]
        val_files = files[split_index:]

        for f in train_files:
            shutil.copy(os.path.join(class_path, f), os.path.join(processed_path, 'train', class_name, f))
        for f in val_files:
            shutil.copy(os.path.join(class_path, f), os.path.join(processed_path, 'val', class_name, f))
    print("Dataset split complete.")

# --- 3. MODEL TRAINING ---

def train_model():
    """Main function to run the model training and validation."""
    
    # Check for GPU availability
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Data augmentation and normalization for training
    # Just normalization for validation
    data_transforms = {
        'train': transforms.Compose([
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
        'val': transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
    }
    
    # Load datasets using ImageFolder
    image_datasets = {x: datasets.ImageFolder(os.path.join(PROCESSED_DATASET_PATH, x), data_transforms[x])
                      for x in ['train', 'val']}
    
    # Create data loaders to feed data in batches
    dataloaders = {x: DataLoader(image_datasets[x], batch_size=BATCH_SIZE, shuffle=True, num_workers=4)
                   for x in ['train', 'val']}
    
    dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'val']}
    class_names = image_datasets['train'].classes
    num_classes = len(class_names)
    print(f"Found {num_classes} classes: {', '.join(class_names[:5])}...")

    # Load the pre-trained model
    model = timm.create_model(MODEL_NAME, pretrained=True, num_classes=num_classes)
    model = model.to(device)

    # Define loss function and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

    # --- Training Loop ---
    best_val_accuracy = 0.0

    for epoch in range(NUM_EPOCHS):
        print(f"\n--- Epoch {epoch + 1}/{NUM_EPOCHS} ---")
        
        for phase in ['train', 'val']:
            if phase == 'train':
                model.train()  # Set model to training mode
            else:
                model.eval()   # Set model to evaluate mode

            running_loss = 0.0
            running_corrects = 0

            # Iterate over data with a progress bar
            for inputs, labels in tqdm(dataloaders[phase], desc=f"{phase.capitalize()}"):
                inputs = inputs.to(device)
                labels = labels.to(device)
                
                optimizer.zero_grad() # Clear gradients

                # Forward pass
                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)

                    # Backward pass + optimize only if in training phase
                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                # Statistics
                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)

            epoch_loss = running_loss / dataset_sizes[phase]
            epoch_acc = running_corrects.double() / dataset_sizes[phase]

            print(f"{phase.capitalize()} Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}")

            # Save the model if it has the best validation accuracy so far
            if phase == 'val' and epoch_acc > best_val_accuracy:
                best_val_accuracy = epoch_acc
                torch.save(model.state_dict(), f"best_model_temp.pth")
                print(f"New best validation accuracy: {best_val_accuracy:.4f}. Model saved.")

    print("\nTraining complete.")
    print(f"Best Validation Accuracy: {best_val_accuracy:.4f}")

    # Load the best model weights and save the final model
    model.load_state_dict(torch.load("best_model_temp.pth"))
    torch.save(model.state_dict(), OUTPUT_MODEL_FILE)
    print(f"Best model saved to '{OUTPUT_MODEL_FILE}'")
    os.remove("best_model_temp.pth") # Clean up temporary file

if __name__ == '__main__':
    # Step 1: Split the raw dataset into train/val folders
    split_dataset(SOURCE_DATASET_PATH, PROCESSED_DATASET_PATH, VALIDATION_SPLIT)
    
    # Step 2: Run the training process
    train_model()