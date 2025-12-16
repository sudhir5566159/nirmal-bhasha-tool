import streamlit as st
import requests  # Direct API calls
from groq import Groq
import anthropic
import json
import csv
import os
from datetime import datetime
import time

# --- AUTHENTICATION ---
# Smart Key Finder
GEMINI_KEY = None
possible_names = ["GEMINI_API_KEY", "GOOGLE_API_KEY", "GEMINI_KEY", "GOOGLE_KEY"]

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
    file_name = "feedback_log.csv"
    try:
        with open(file_name, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if not os.path.isfile(file_name):
                writer.writerow(["Date", "Tool Name", "Rating", "User Input", "AI Output", "Comments"])
            writer.writerow([datetime.now(), tool_name, rating, user_input, ai_output, comment])
            return True
    except:
        return False

# --- DIRECT API CALL FUNCTION ---
def call_gemini_direct(model_name, prompt):
    # Standard URL for Google AI Studio keys
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={GEMINI_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
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
        # Return the specific error from Google
        raise Exception(f"Google Error {response.status_code}: {response.text}")

# --- MAIN AI RESPONSE LOGIC ---
def get_ai_response(system_prompt, user_text, engine):
    
    def make_busy_message(e1, e2):
        return f"""
        ### ⚠️ High Traffic Alert (अत्यधिक ट्रैफिक चेतावनी)
        Due to overwhelming demand, our AI servers are running at full capacity.
        #### ⏳ Please wait 60 seconds and try again.
        
        <br><hr>
        <details>
        <summary>👨‍💻 Debug Info</summary>
        <div style='color:red; font-size:12px; font-family:monospace;'>
        <b>Attempt 1 (Gemini Pro):</b> {str(e1)}<br><br>
        <b>Attempt 2 (Gemini 1.0 Pro):</b> {str(e2)}
        </div>
        </details>
        """

    try:
        is_ok, count = check_word_count(user_text)
        if not is_ok:
            return f"⚠️ **Limit Exceeded:** Your text has **{count} words**. Limit is **{MAX_WORD_LIMIT}**."

        # OPTION 1: GOOGLE GEMINI
        if "Gemini" in engine:
            if not GEMINI_KEY: 
                return "❌ **Setup Error:** No API Key found. Please add `GEMINI_API_KEY` to Secrets."
            
            full_prompt = system_prompt + "\n\nUser Input: " + user_text
            
            # ATTEMPT 1: Try "gemini-pro" (The original, most compatible model)
            try:
                return call_gemini_direct("gemini-pro", full_prompt)
            except Exception as e1:
                
                # ATTEMPT 2: Try "gemini-1.0-pro" (The alternative name)
                try:
                    return call_gemini_direct("gemini-1.0-pro", full_prompt)
                except Exception as e2:
                    return make_busy_message(e1, e2)

        # OPTION 2: LLAMA (Groq)
        elif "Llama" in engine or "Groq" in engine:
            if not groq_client: return "Error: Groq API Key missing."
            try:
                completion = groq_client.chat.completions.create(
                    messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_text}],
                    model="llama-3.3-70b-versatile", temperature=0.3
                )
                return completion.choices[0].message.content
            except:
                 return "⚠️ Groq Service Busy."

        # OPTION 3: CLAUDE
        elif "Claude" in engine:
            if not anthropic_client: return "Error: Anthropic API Key missing."
            try:
                message = anthropic_client.messages.create(
                    model="claude-3-5-sonnet-20240620", max_tokens=1024, system=system_prompt,
                    messages=[{"role": "user", "content": user_text}]
                )
                return message.content[0].text
            except:
                return "⚠️ Claude Service Busy."
        else:
            return "Error: Unknown Engine Selected"
            
    except Exception as e:
        return f"System Error: {str(e)}"
