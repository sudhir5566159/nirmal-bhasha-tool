import streamlit as st
import requests
from groq import Groq
import anthropic
import json
import csv
import os
from datetime import datetime
import time

# --- AUTHENTICATION ---
GEMINI_KEY = None
possible_names = ["GEMINI_API_KEY", "GOOGLE_API_KEY", "GEMINI_KEY"]
for name in possible_names:
    if name in st.secrets:
        GEMINI_KEY = st.secrets[name]
        break

GROQ_KEY = st.secrets.get("GROQ_API_KEY", "")
ANTHROPIC_KEY = st.secrets.get("ANTHROPIC_API_KEY", "")

# Initialize Clients
groq_client = Groq(api_key=GROQ_KEY) if GROQ_KEY else None
try:
    anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_KEY) if ANTHROPIC_KEY else None
except:
    anthropic_client = None

# --- CONSTANTS ---
MAX_WORD_LIMIT = 1000 
POE_LINK = "https://poe.com/Nirmal-Bhasha"

# --- HELPER: FALLBACK MESSAGE (Custom Text + Logo) ---
def get_fallback_message(error_type, details=""):
    """
    Returns a High-Visibility Markdown message with the specific Poe link text.
    """
    return f"""
# ⚠️ System Busy / सर्वर व्यस्त है

**Don't worry! You can still use the app instantly.**
*(चिंता न करें! आप अभी भी ऐप का उपयोग कर सकते हैं।)*

Our free server is currently overloaded. We have a **Premium High-Speed Backup** available for free on Poe.com.

## 👉 [🚀 CLICK HERE to Continue the same Nirmal Bhasha 🌸 on Poe.com without any disruption]({POE_LINK})
*(Clicking above will open the backup server, which never gets stuck)*

---
<small>Technical Error: {error_type} | {details}</small>
    """

# --- HELPER FUNCTIONS ---
def check_word_count(text):
    word_count = len(text.split())
    if word_count > MAX_WORD_LIMIT:
        return False, word_count
    return True, word_count

def load_correction_rules():
    try:
        with open("corrections.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return str(data["correction_rules"])
    except:
        return "No correction rules found."

def save_feedback(tool_name, user_input, ai_output, rating, comment=""):
    try:
        file_name = "feedback_log.csv"
        with open(file_name, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if not os.path.isfile(file_name):
                writer.writerow(["Date", "Tool Name", "Rating", "User Input", "AI Output", "Comments"])
            writer.writerow([datetime.now(), tool_name, rating, user_input, ai_output, comment])
            return True
    except:
        return False

# --- DIRECT GEMINI API CALL ---
def call_gemini_direct(model_name, prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={GEMINI_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "safetySettings": [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        raise Exception(f"Google Error {response.status_code}: {response.text}")

# --- MAIN LOGIC ---
def get_ai_response(system_prompt, user_text, engine):
    
    try:
        # 1. CHECK WORD LIMIT
        is_ok, count = check_word_count(user_text)
        if not is_ok: 
            return get_fallback_message("Limit Exceeded", f"Text is {count} words.")

        # OPTION 1: GEMINI (Google)
        if "Gemini" in engine:
            if not GEMINI_KEY: return get_fallback_message("Setup Error", "API Key Missing.")
            full_prompt = system_prompt + "\n\nUser Input: " + user_text
            
            # Try 2.5 Flash -> 2.0 Flash -> Poe Fallback
            try: return call_gemini_direct("gemini-2.5-flash", full_prompt)
            except Exception as e1:
                try: return call_gemini_direct("gemini-2.0-flash", full_prompt)
                except Exception as e2:
                    return get_fallback_message("Connection Failed", "Google Servers Busy")

        # OPTION 2: LLAMA (via Groq)
        elif "Llama" in engine or "Groq" in engine:
            if not groq_client: return get_fallback_message("Setup Error", "Groq Key Missing")
            
            try:
                completion =
