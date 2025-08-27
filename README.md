# anime
identify character


anime_character_recognizer/
├── app/
│   ├── __init__.py
│   └── main.py
├── pretrained_model.pth
└── requirements.txt

# AI-Powered Anime Character Recognizer

## 📌 Project Overview

The **AI-Powered Anime Character Recognizer** is a full-stack web application that identifies anime characters from uploaded images. Once recognized, it generates a detailed profile including:

* Biography and physical attributes
* Anime details
* Direct streaming links
* AI-generated tags for style/appearance
* Suggestions of visually similar characters

This project demonstrates the integration of **deep learning**, **LLMs (Google Gemini)**, and **external APIs (Jikan)** into a seamless end-to-end prototype.

---

## 🏗️ System Architecture

The application is built on a modern client-server architecture with three main components:

* **Frontend (React + Tailwind CSS):** Single-page application for image upload & results display.
* **Backend (FastAPI + PyTorch):** Orchestrates recognition pipeline, AI enrichment, and API calls.
* **AI Models & APIs:** Deep learning for recognition, Gemini API for enrichment, Jikan API for images.

---

## ⚙️ Technology Stack

### Backend (Python)

* Framework: **FastAPI**
* Web Server: **Uvicorn**
* Deep Learning: **PyTorch**, **timm (EfficientNet-B0)**
* Image Processing: **Pillow**
* Config: **pydantic-settings**, **python-dotenv**
* APIs: **requests**, **google-generativeai**
* Similarity: **scipy (initially)**, replaced with **Jaccard Distance**

### Frontend (JavaScript)

* Framework: **React (Vite)**
* Styling: **Tailwind CSS**
* Package Manager: **npm**

### External APIs

* **Google Gemini API:** Provides enriched JSON (bio, tags, anime name, streaming links).
* **Jikan API:** Fetches anime character images without authentication.

---

## 🔄 Workflow (End-to-End)

1. **Image Upload (Frontend):** User uploads anime character image.
2. **API Request:** Image sent to FastAPI backend `/recognize` endpoint.
3. **Recognition (Backend):**

   * Preprocess image → EfficientNet-B0 → Predict character.
   * Confidence check (>60% required).
4. **Data Enrichment (Gemini):**

   * Character name sent to Gemini API.
   * Returns structured JSON with biography, tags, anime, streaming links.
5. **Similarity Search:**

   * Jaccard Distance used on AI-generated tags.
   * Top 3 visually similar characters selected.
6. **Image Retrieval (Jikan):**

   * Images fetched for main and similar characters.
7. **Final Response:**

   * Consolidated JSON returned (character profile, images, links).
8. **Frontend Display:**

   * Results dynamically rendered with profile, streaming links, and similar characters gallery.

---

## 🧩 Detailed Components

### 🔹 Deep Learning Model

* Fine-tuned **EfficientNet-B0** trained on custom anime dataset.
* `class_names.json` maps model outputs (IDs) to character names.

### 🔹 Prompt Engineering (Gemini)

* Structured prompts ensure clean JSON.
* Includes example formats to avoid chatbot-like responses.

### 🔹 Similarity Algorithm

* Initially **Wasserstein distance** (incorrect for categorical data).
* Replaced with **Jaccard Distance** → compares tag sets efficiently.

### 🔹 Decoupled Services

* `gemini_service.py`, `jikan_service.py`, etc.
* Modular design → easy debugging and swapping services.

---

## 🚀 Installation & Setup

### Backend

```bash
# Clone repository
git clone <repo_url>
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)

# Install dependencies
pip install -r requirements.txt

# Run FastAPI server
uvicorn app:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 📊 Example API Response

```json
{
  "character": "Goku",
  "confidence": 0.92,
  "about": "A Saiyan warrior...",
  "anime_name": "Dragon Ball Z",
  "streaming_platforms": [
    {"name": "Crunchyroll", "url": "https://..."}
  ],
  "tags": ["spiky hair", "orange outfit", "energetic"],
  "similar_characters": [
    {"name": "Naruto", "image_url": "https://..."},
    {"name": "Ichigo Kurosaki", "image_url": "https://..."}
  ],
  "image_url": "https://..."
}
```

---

## ✅ Conclusion

The **AI-Powered Anime Character Recognizer** showcases how **deep learning**, **LLMs**, and **modern web stacks** can be combined to build an intelligent, scalable, and interactive anime recognition system. While recognition accuracy depends on dataset quality, the **architecture and pipeline are robust, modular, and production-ready**.

---

## 📌 Future Improvements

* Expand dataset for higher recognition accuracy.
* Optimize inference with ONNX/TensorRT.
* Add support for multiple characters in one image.
* User authentication & personalized history.
