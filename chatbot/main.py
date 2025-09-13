from fastapi import FastAPI, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import google.generativeai as genai
from dotenv import load_dotenv
import os

# ✅ Load .env file
load_dotenv()

# ✅ Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("⚠️ Please set GEMINI_API_KEY in a .env file or environment variable")

print("API Key loaded succesfully")
genai.configure(api_key=api_key)
app = FastAPI()

# ✅ Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Serve static files (for audio responses etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")


# 🧠 Gemini chat function
def ask_gemini(prompt: str) -> str:
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")  # or "gemini-1.5-pro"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Gemini API Error: {str(e)}"


# 📝 Text chat endpoint
@app.post("/text-chat")
async def text_chat(request: Request):
    body = await request.json()
    message = body.get("message", "")

    if not message:
        return {"text": "⚠️ Please enter a message."}

    prompt = f"You are a helpful assistant. Respond to the farmer's query: {message}"
    answer = ask_gemini(prompt)

    return {"text": answer}


# 🎤 Voice chat endpoint (placeholder for now)
@app.post("/voice-chat")
async def voice_chat(file: UploadFile):
    return {"text": "Voice chat not implemented yet with Gemini."}
