import streamlit as st
import google.generativeai as genai
from groq import Groq
import json

# --- AUTHENTICATION ---
# 1. Google Gemini
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    pass # Handle errors silently if key is missing

# 2. Groq (Meta Llama 3)
try:
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    groq_client = None

# --- HEADER FUNCTION ---
def show_header():
    col1, col2 = st.columns([1, 5])
    with col1:
        # Shows the uploaded logo if available, otherwise a default emoji
        try:
            st.image("nirmal_logo.png", width=60)
        except:
            st.write("🪷")
    with col2:
        st.markdown("""
            <h3 style='margin-bottom:0; color: #ff4b4b;'>ShabdaSankalan AI</h3>
            <p style='margin-top:0; font-size: 14px; color: gray;'>The Digital Infrastructure for Hindi Language</p>
            """, unsafe_allow_html=True)
    st.markdown("---")

# --- AI RESPONSE FUNCTION ---
def get_ai_response(system_prompt, user_text, engine):
    try:
        # OPTION 1: GOOGLE GEMINI (The Default)
        if "Gemini" in engine:
            model = genai.GenerativeModel("gemini-2.0-flash-exp")
            response = model.generate_content(system_prompt + "\n\nUser Input: " + user_text)
            return response.text

        # OPTION 2: META LLAMA 3 (via Groq)
        elif "Llama" in engine or "Meta" in engine:
            if not groq_client:
                return "Error: Groq API Key not found in Secrets."
            
            completion = groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_text}
                ],
                model="llama3-70b-8192", # Using the big powerful version
            )
            return completion.choices[0].message.content

        # OPTION 3: OPENAI (Paid)
        elif "GPT" in engine:
            return "OpenAI is currently not connected (Paid Tier required)."

        else:
            return "Error: Unknown Engine Selected"

    except Exception as e:
        return f"Error: {str(e)}"

# --- LOAD CORRECTIONS ---
def load_correction_rules():
    try:
        with open("corrections.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return str(data["correction_rules"])
    except:
        return "No correction rules found."
