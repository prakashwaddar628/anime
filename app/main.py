import io
import json
from fastapi import FastAPI, UploadFile, File, HTTPException
from PIL import Image
import torch
import timm
from torchvision import transforms
from fastapi.middleware.cors import CORSMiddleware

# Import all three of our services
from .services import gemini_service, similarity_service, jikan_service

# --------------------------------------------------------------------------
# (Sections 1-4: App, Class Names, Model, Transforms - remain the same)
# --------------------------------------------------------------------------
# 1. Initialize the FastAPI App
app = FastAPI(
    title="Anime Character Recognizer API",
    description="Full pipeline API to identify characters, get details, find similar ones, and provide image URLs.",
    version="1.0.0",
)

origins = [
    "http://localhost:5173",
    "http://localhost:3000", # Common for other React dev servers
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods (GET, POST, etc.)
    allow_headers=["*"], # Allows all headers
)

# 2. Load Class Names
try:
    with open("class_names.json", "r") as f:
        class_names = json.load(f)
    NUM_CLASSES = len(class_names)
except FileNotFoundError:
    raise RuntimeError("Could not find class_names.json.")

# 3. Load the Fine-Tuned Model
model = timm.create_model('efficientnet_b0', pretrained=False, num_classes=NUM_CLASSES)

# --- THIS IS THE KEY CHANGE ---
# Load the weights you just trained
try:
    model.load_state_dict(torch.load('anime_character_model.pth', map_location=torch.device('cpu')))
    print("--- Successfully loaded fine-tuned model weights! ---")
except FileNotFoundError:
    print("--- WARNING: anime_character_model.pth not found. Running in simulation mode. ---")
# ----------------------------

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
    return {"status": "ok", "message": "API is fully operational"}


@app.post("/recognize")
async def recognize_character(file: UploadFile = File(...)):
    """
    The main endpoint that orchestrates the entire recognition pipeline.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File is not an image.")

    try:
        # --- 1. Model Prediction ---
        image_content = await file.read()
        image = Image.open(io.BytesIO(image_content)).convert("RGB")
        image_tensor = transform(image).unsqueeze(0)

        with torch.no_grad():
            output = model(image_tensor)
        
        probabilities = torch.nn.functional.softmax(output[0], dim=0)
        predicted_class_idx = output.argmax(-1).item()
        predicted_character_name = class_names.get(str(predicted_class_idx), "Unknown Character")
        confidence = probabilities[predicted_class_idx].item()
        
        # --- NEW: CONFIDENCE THRESHOLD CHECK ---
        CONFIDENCE_THRESHOLD = 0.20  # This is 60%

        if confidence < CONFIDENCE_THRESHOLD:
            # If the model's confidence is too low, stop everything and return an error.
            # Our frontend will display this 'detail' message.
            raise HTTPException(
                status_code=404,
                detail=f"Unidentified character. (Confidence: {confidence:.2%}) is below the {CONFIDENCE_THRESHOLD:.0%} threshold."
            )
        # ----------------------------------------

        if predicted_character_name == "Unknown Character":
            # This is a fallback for a different kind of error (e.g., bad class index)
            raise HTTPException(status_code=500, detail="Character index out of bounds.")

        # --- 2. Get Details from Gemini ---
        character_details = gemini_service.get_character_details_from_gemini(predicted_character_name)
        if "error" in character_details:
            raise HTTPException(status_code=502, detail=f"Gemini API Error: {character_details['error']}")
            
        # --- 3. Find Similar Characters ---
        predicted_tags = character_details.get("tags", [])
        similar_characters = similarity_service.find_similar_characters(
            predicted_character_name=character_details.get("name"),
            predicted_character_tags=predicted_tags
        )
        
        # --- 4. Enrich with Image URLs from Jikan ---
        main_char_name_for_search = character_details.get("name", predicted_character_name)
        character_details["image_url"] = jikan_service.get_character_image_url(main_char_name_for_search)
        
        for char in similar_characters:
            char["image_url"] = jikan_service.get_character_image_url(char["name"])

        # --- 5. Combine and Return Full Response ---
        return {
            "prediction_result": {
                "predicted_character": predicted_character_name,
                "confidence": f"{confidence:.2%}",
            },
            "character_details": character_details,
            "similar_characters": similar_characters
        }

    except Exception as e:
        # This will catch our HTTPException and any other errors
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"An error occurred during the process: {str(e)}")