import streamlit as st
import google.generativeai as genai
from groq import Groq
import anthropic
import json

# --- AUTHENTICATION ---
# 1. Google Gemini
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    pass 

# 2. Groq (Meta Llama 3)
try:
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    groq_client = None

# 3. Anthropic (Claude)
try:
    anthropic_client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
except:
    anthropic_client = None

# --- HEADER FUNCTION ---
def show_header():
    col1, col2 = st.columns([1, 5])
    with col1:
        try:
            st.image("nirmal_logo.png", width=60)
        except:
            pass 
    with col2:
        st.markdown("""
            <h3 style='margin-bottom:0; color: #ff4b4b;'>ShabdaSankalan AI</h3>
            <p style='margin-top:0; font-size: 14px; color: gray;'>The Digital Infrastructure for Hindi Language</p>
            """, unsafe_allow_html=True)
    st.markdown("---")

# --- AI RESPONSE FUNCTION ---
def get_ai_response(system_prompt, user_text, engine):
    try:
        # OPTION 1: GOOGLE GEMINI (The Best for Hindi)
        if "Gemini" in engine:
            # FIX: Using 'gemini-1.5-flash-latest' which is the safest alias
            model = genai.GenerativeModel("gemini-1.5-flash-latest")
            response = model.generate_content(system_prompt + "\n\nUser Input: " + user_text)
            return response.text

        # OPTION 2: META LLAMA 3 (via Groq)
        elif "Llama" in engine or "Groq" in engine:
            if not groq_client:
                return "Error: Groq API Key not found in Secrets."
            
            completion = groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_text}
                ],
                # Using the newest versatile model
                model="llama-3.3-70b-versatile", 
                temperature=0.3, # Lower temperature = stricter, less hallucination
            )
            return completion.choices[0].message.content

        # OPTION 3: CLAUDE (Paid)
        elif "Claude" in engine:
            if not anthropic_client:
                return "Error: Anthropic API Key not found."
            
            message = anthropic_client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=1024,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_text}
                ]
            )
            return message.content[0].text

        else:
            return "Error: Unknown Engine Selected"

    except Exception as e:
        # If Gemini fails, give a clear hint
        if "404" in str(e) and "Gemini" in engine:
            return f"Error: Model ID not found. Try updating requirements.txt. Details: {str(e)}"
        return f"Error: {str(e)}"

# --- LOAD CORRECTIONS ---
def load_correction_rules():
    try:
        with open("corrections.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return str(data["correction_rules"])
    except:
        return "No correction rules found."
