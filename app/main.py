import io
import json
from fastapi import FastAPI, UploadFile, File, HTTPException
from PIL import Image
import torch
import timm
from torchvision import transforms

# Import the new Gemini service
from .services import gemini_service

# --------------------------------------------------------------------------
# (Sections 1-4: App, Class Names, Model, Transforms - remain the same)
# ... [No changes needed in the first 4 sections of the file] ...
# --------------------------------------------------------------------------
# 1. Initialize the FastAPI App
app = FastAPI(
    title="Anime Character Recognizer API",
    description="An API that uses a fine-tuned model to identify anime characters and get their details.",
    version="0.3.0",
)

# 2. Load Class Names and Model Configuration
try:
    with open("class_names.json", "r") as f:
        class_names = json.load(f)
    NUM_CLASSES = len(class_names)
except FileNotFoundError:
    raise RuntimeError("Could not find class_names.json. Please create it.")

# 3. Load the Fine-Tuned Model
model = timm.create_model('efficientnet_b0', pretrained=False, num_classes=NUM_CLASSES)
print("--- SIMULATION MODE ---")
model.eval()

# 4. Define Image Transformations
model_config = model.default_cfg
transform = transforms.Compose([
    transforms.Resize(model_config['input_size'][1:]),
    transforms.CenterCrop(model_config['input_size'][1:]),
    transforms.ToTensor(),
    transforms.Normalize(mean=model_config['mean'], std=model_config['std']),
])


# --------------------------------------------------------------------------
# 5. Define the Endpoints
# --------------------------------------------------------------------------
@app.get("/")
def read_root():
    """A simple endpoint to check if the API is running."""
    return {"status": "ok", "message": "Welcome to the Anime Character Recognizer API"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Receives an image, predicts the character, and fetches details from Gemini.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File provided is not an image.")

    try:
        # --- Model Prediction Logic (from previous step) ---
        image_content = await file.read()
        image = Image.open(io.BytesIO(image_content)).convert("RGB")
        image_tensor = transform(image).unsqueeze(0)

        with torch.no_grad():
            output = model(image_tensor)
        
        probabilities = torch.nn.functional.softmax(output[0], dim=0)
        predicted_class_idx = output.argmax(-1).item()
        
        predicted_character_name = class_names.get(str(predicted_class_idx), "Unknown Character")
        confidence = probabilities[predicted_class_idx].item()
        
        if predicted_character_name == "Unknown Character":
            raise HTTPException(status_code=404, detail="Character could not be identified.")

        # --- NEW: Call Gemini Service ---
        # Take the predicted name and get the detailed profile.
        character_details = gemini_service.get_character_details_from_gemini(predicted_character_name)

        if "error" in character_details:
             # If Gemini fails, return the error but still include the prediction
            return {
                "prediction_result": {
                    "predicted_character": predicted_character_name,
                    "confidence": f"{confidence:.2%}",
                },
                "details_error": character_details["error"]
            }
            
        # --- Combine and return the full response ---
        return {
            "prediction_result": {
                "predicted_character": predicted_character_name,
                "confidence": f"{confidence:.2%}",
            },
            "character_details": character_details
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")