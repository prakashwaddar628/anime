from fastapi import FastAPI

# Initialize the FastAPI app
app = FastAPI(
    title="Anime Character Recognizer API",
    description="An API that uses a DL model to identify an anime character from an image.",
    version="0.1.0",
)

@app.get("/")
def read_root():
    """A simple endpoint to check if the API is running."""
    return {"status": "ok", "message": "Welcome to the Anime Character Recognizer API"}