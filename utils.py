import streamlit as st
import google.generativeai as genai
import openai
import anthropic
import json

# --- SHARED: LOGO DISPLAY FUNCTION ---
def show_header():
    # CSS to hide default Streamlit branding
    st.markdown("""
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 5])
    with col1:
        # SVG Logo (Pink Lotus)
        st.markdown("""
            <div style="display: flex; justify-content: center;">
                <svg width="70" height="70" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                    <path d="M50 10 C50 10 30 40 10 50 C30 60 50 90 50 90 C50 90 70 60 90 50 C70 40 50 10 50 10 Z" fill="#E91E63" stroke="#C2185B" stroke-width="2"/>
                    <circle cx="50" cy="50" r="5" fill="#FFC107" />
                    <path d="M50 90 Q30 80 20 60 M50 90 Q70 80 80 60" stroke="#4CAF50" stroke-width="3" fill="none"/>
                </svg>
            </div>
            """, unsafe_allow_html=True)
    with col2:
        st.title("ShabdaSankalan AI")
        st.caption("The Digital Infrastructure for Hindi Language")
    st.markdown("---")

# --- SHARED: AI API LOGIC ---
def get_ai_response(system_prompt, user_prompt, model_choice):
    try:
        if "Gemini" in model_choice:
            genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
            model = genai.GenerativeModel('gemini-2.0-flash') 
            return model.generate_content(f"{system_prompt}\n\nUser Input: {user_prompt}").text

        elif "OpenAI" in model_choice:
            client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]
            )
            return response.choices[0].message.content

        elif "Anthropic" in model_choice:
            client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
            msg = client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=1000,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            return msg.content[0].text
    except Exception as e:
        return f"Error: {str(e)}"

# --- SHARED: LOAD CORRECTIONS ---
def load_correction_rules():
    try:
        with open('corrections.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            rules_text = ""
            for rule in data['correction_rules']:
                rules_text += f"- If you see '{rule['word']}', Origin is {rule['origin']}. Replacement: '{rule['replacement']}'.\n"
            return rules_text
    except:
        return ""