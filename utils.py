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

def get_daily_word():
    words = [
        {"word": "Jijivisha (जिजीविषा)", "meaning": "Strong desire to live (जीने की प्रबल इच्छा)."},
        {"word": "Kritagya (कृतज्ञ)", "meaning": "One who is grateful (उपकार मानने वाला)."},
        {"word": "Mumukshu (मुमुक्षु)", "meaning": "One who desires salvation (मोक्ष का इच्छुक)."},
        {"word": "Titiksha (तितिक्षा)", "meaning": "Patience/Endurance (सहन करने की शक्ति)."},
        {"word": "Anivarchaniya (अनिर्वचनीय)", "meaning": "Indescribable (जो वाणी द्वारा वर्णन न किया जा सके)."}
    ]
    day_of_year = datetime.now().timetuple().tm_yday
    return words[day_of_year % len(words)]

def save_subscriber(email):
    file_name = "subscribers.csv"
    try:
        with open(file_name, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if not os.path.isfile(file_name):
                writer.writerow(["Date", "Email"])
            writer.writerow([datetime.now(), email])
            return True
    except:
        return False

def show_header():
    col1, col2 = st.columns([1, 5])
    with col1:
        try: st.image("nirmal_logo.png", width=60)
        except: st.markdown("<div style='font-size: 40px;'>🌸</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <h3 style='margin-bottom:0; color: #ff4b4b;'>ShabdaSankalan AI</h3>
            <p style='margin-top:0; font-size: 14px; color: gray;'>The Digital Infrastructure for Hindi Language</p>
            """, unsafe_allow_html=True)
    st.markdown("---")

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

# --- SMART AI RESPONSE (Bulletproof Logic) ---
def get_ai_response(system_prompt, user_text, engine):
    try:
        # Check Limits
        is_ok, count = check_word_count(user_text)
        if not is_ok:
            return f"⚠️ **Limit Exceeded:** Your text has **{count} words**. Limit is **{MAX_WORD_LIMIT}**."

        # OPTION 1: GOOGLE GEMINI (Smart Fallback Strategy)
        if "Gemini" in engine:
            
            # Unblock safety filters to prevent false positives on Hindi text
            safety_settings = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]

            # ATTEMPT 1: Try Gemini 2.0 Flash (Experimental)
            try:
                # Exact Name: gemini-2.0-flash-exp
                model = genai.GenerativeModel("gemini-2.0-flash-exp")
                response = model.generate_content(
                    system_prompt + "\n\nUser Input: " + user_text,
                    safety_settings=safety_settings
                )
                return response.text
            except:
                # ATTEMPT 2: Fallback to Gemini 1.5 Flash (Stable & High Limit)
                try:
                    # Exact Name: gemini-1.5-flash
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content(
                        system_prompt + "\n\nUser Input: " + user_text,
                        safety_settings=safety_settings
                    )
                    return response.text
                except Exception as e:
                    return f"Server Busy (Quota Exceeded). Please try again in 1 minute. Error: {str(e)}"

        # OPTION 2: META LLAMA 3 (via Groq)
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
