import streamlit as st
import google.generativeai as genai
from groq import Groq
import anthropic
import json
import csv
import os
from datetime import datetime
import time

# --- AUTHENTICATION ---
# Check if keys exist
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    pass 

try:
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    groq_client = None

try:
    anthropic_client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
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

# --- DIAGNOSTIC AI RESPONSE (Shows Real Errors) ---
def get_ai_response(system_prompt, user_text, engine):
    try:
        is_ok, count = check_word_count(user_text)
        if not is_ok:
            return f"⚠️ **Limit Exceeded:** {count} words."

        # OPTION 1: GOOGLE GEMINI (Diagnostic Mode)
        if "Gemini" in engine:
            try:
                # 1. Use the STABLE Model
                model = genai.GenerativeModel("gemini-1.5-flash")
                
                # 2. Safety Settings
                safety_settings = [
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                ]

                response = model.generate_content(
                    system_prompt + "\n\nUser Input: " + user_text,
                    safety_settings=safety_settings
                )
                return response.text
            except Exception as e:
                # SHOW THE REAL ERROR (Don't hide it behind 'Busy')
                return f"❌ **Technical Error:** {str(e)}\n\n*Please check your API Key in .streamlit/secrets.toml*"

        # OPTION 2: LLAMA
        elif "Llama" in engine or "Groq" in engine:
            if not groq_client: return "Error: Groq API Key missing."
            completion = groq_client.chat.completions.create(
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_text}],
                model="llama-3.3-70b-versatile", temperature=0.3
            )
            return completion.choices[0].message.content

        # OPTION 3: CLAUDE
        elif "Claude" in engine:
            if not anthropic_client: return "Error: Anthropic API Key missing."
            message = anthropic_client.messages.create(
                model="claude-3-5-sonnet-20240620", max_tokens=1024, system=system_prompt,
                messages=[{"role": "user", "content": user_text}]
            )
            return message.content[0].text
            
        else:
            return "Error: Unknown Engine Selected"
            
    except Exception as e:
        return f"System Error: {str(e)}"
