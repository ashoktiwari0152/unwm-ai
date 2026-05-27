from arcrs.recursive_engine import recursive_analysis
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
from dotenv import load_dotenv
from langdetect import detect

import os
import json
from datetime import datetime

# ============================================
# LOAD ENV
# ============================================

load_dotenv()

# ============================================
# API KEY
# ============================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ============================================
# GROQ CLIENT
# ============================================

client = Groq(
    api_key=GROQ_API_KEY
)

# ============================================
# FASTAPI APP
# ============================================

app = FastAPI(
    title="UNWM AI"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# CORS
# ============================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# CHAT HISTORY FILE
# ============================================

CHAT_HISTORY_FILE = "chat_history.json"

# Create history file if not exists
if not os.path.exists(CHAT_HISTORY_FILE):

    with open(
        CHAT_HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump([], f)

# ============================================
# REQUEST MODEL
# ============================================

class PromptRequest(BaseModel):

    topic: str
    depth: str = "normal"

# ============================================
# LANGUAGE DETECTION
# ============================================

def detect_language(text):

    text_lower = text.lower()

    # Hinglish words
    hinglish_words = [
        "main",
        "mera",
        "mujhe",
        "tum",
        "kya",
        "kaise",
        "kon",
        "hu",
        "hain",
        "nahi",
        "kyu",
        "acha",
        "bhai"
    ]

    # Hinglish detection first
    if any(word in text_lower for word in hinglish_words):
        return "Hinglish"

    try:

        lang = detect(text)

        language_map = {
            "en": "English",
            "fr": "French",
            "hi": "Hindi",
            "mr": "Marathi",
            "ja": "Japanese",
            "ko": "Korean",
            "zh-cn": "Chinese",
            "zh-tw": "Chinese",
            "es": "Spanish",
            "de": "German",
            "ru": "Russian",
            "ar": "Arabic",
            "pt": "Portuguese",
            "it": "Italian"
        }

        return language_map.get(
            lang,
            "English"
        )

    except:

        return "English"

# ============================================
# GET RECENT HISTORY
# ============================================

def get_recent_history(limit=5):

    try:

        with open(
            CHAT_HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            chats = json.load(f)

        recent_chats = chats[-limit:]

        history_text = ""

        for chat in recent_chats:

            history_text += f"""

User: {chat['topic']}

AI: {chat['response']}

"""

        return history_text

    except:

        return ""

# ============================================
# SAVE CHAT HISTORY
# ============================================

def save_chat(topic, response, language):

    try:

        with open(
            CHAT_HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            chats = json.load(f)

        chats.append({

            "timestamp": str(datetime.now()),
            "topic": topic,
            "language": language,
            "response": response

        })

        with open(
            CHAT_HISTORY_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                chats,
                f,
                indent=4,
                ensure_ascii=False
            )

    except Exception as e:

        print("Chat Save Error:", e)

# ============================================
# ASK GROQ
# ============================================

def ask_groq(topic, depth):

    final_language = detect_language(topic)

    # Load previous chats
    conversation_history = get_recent_history()

    prompt = f"""
You are UNWM AI v2.

Previous Conversation:
{conversation_history}

Current User Question:
{topic}

Depth:
{depth}

Rules:

1. If language is Hinglish,
   respond in casual Hinglish using Hindi words in English letters.

2. Otherwise respond ONLY in {final_language}.

3. Never switch language.

4. Remember previous conversation context.

5. Continue conversation naturally.

6. Give deep philosophical and intelligent responses.

7. Keep response clean and readable.

8. Use headings and structure.
"""

    completion = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.7,
        max_tokens=2000

    )

    answer = completion.choices[0].message.content

    # Save chat
    save_chat(
        topic,
        answer,
        final_language
    )

    return answer

# ============================================
# HOME ROUTE
# ============================================

@app.get("/")
async def root():

    return {
        "message": "UNWM AI Backend Running Successfully"
    }

# ============================================
# GENERATE ROUTE
# ============================================

@app.post("/generate")
async def generate(data: PromptRequest):

    analysis = recursive_analysis(data.topic)
    
    ai_response = ask_groq(
        data.topic,
        data.depth
    )

    return {

        "success": True,
        "timestamp": str(datetime.now()),
        "topic": data.topic,
        "depth": data.depth,
        "response": ai_response,
        "recursives_analysis": analysis

    }

# ============================================
# HISTORY ROUTE
# ============================================

@app.get("/history")
async def history():

    with open(
        CHAT_HISTORY_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        chats = json.load(f)

    return chats

# ============================================
# CLEAR HISTORY ROUTE
# ============================================

@app.delete("/clear-history")
async def clear_history():

    with open(
        CHAT_HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump([], f)

    return {
        "message": "Chat history cleared"
    }

# ============================================
# RUN SERVER
# ============================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "backend:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
