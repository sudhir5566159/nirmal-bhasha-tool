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

# --- ROBUST AI RESPONSE (Triple-Fallback Logic) ---
def get_ai_response(system_prompt, user_text, engine):
    
    # CUSTOM BUSY MESSAGE (With Hidden Debug Info)
    def make_busy_message(e1, e2, e3):
        return f"""
        ### ⚠️ High Traffic Alert (अत्यधिक ट्रैफिक चेतावनी)
        Due to overwhelming demand, our AI servers are running at full capacity.
        #### ⏳ Please wait 60 seconds and try again.
        
        <br><hr>
        <details>
        <summary>👨‍💻 Technical Debug Info (Click if you are the Developer)</summary>
        <div style='color:red; font-size:12px; font-family:monospace;'>
        <b>Attempt 1 (Flash 1.5):</b> {str(e1)}<br><br>
        <b>Attempt 2 (Pro 1.5):</b> {str(e2)}<br><br>
        <b>Attempt 3 (Pro 1.0):</b> {str(e3)}
        </div>
        </details>
        """

    try:
        # Check Limits
        is_ok, count = check_word_count(user_text)
        if not is_ok:
            return f"⚠️ **Limit Exceeded:** Your text has **{count} words**. Limit is **{MAX_WORD_LIMIT}**."

        # OPTION 1: GOOGLE GEMINI
        if "Gemini" in engine:
            
            full_prompt = system_prompt + "\n\nUser Input: " + user_text
            
            # ATTEMPT 1: Gemini 1.5 Flash (The Best)
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                # We relax safety settings for the main attempt
                safety_settings = [
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                ]
                response = model.generate_content(full_prompt, safety_settings=safety_settings)
                return response.text
            except Exception as e1:
                
                # ATTEMPT 2: Gemini 1.5 Pro (The Backup)
                try:
                    model = genai.GenerativeModel("gemini-1.5-pro")
                    response = model.generate_content(full_prompt) # No safety settings to reduce errors
                    return response.text
                except Exception as e2:
                    
                    # ATTEMPT 3: Gemini Pro (The Old Reliable)
                    try:
                        model = genai.GenerativeModel("gemini-pro")
                        response = model.generate_content(full_prompt)
                        return response.text
                    except Exception as e3:
                        
                        # ALL 3 FAILED: Show message + Debug info
                        return make_busy_message(e1, e2, e3)

        # OPTION 2: META LLAMA 3
        elif "Llama" in engine or "Groq" in engine:
            if not groq_client: return "Error: Groq API Key missing."
            try:
                completion = groq_client.chat.completions.create(
                    messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_text}],
                    model="llama-3.3-70b-versatile", temperature=0.3
                )
                return completion.choices[0].message.content
            except:
                 return "⚠️ Groq Service Busy. Please try Gemini."

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
                return "⚠️ Claude Service Busy. Please try Gemini."
        else:
            return "Error: Unknown Engine Selected"
            
    except Exception as e:
        return f"System Error: {str(e)}"
