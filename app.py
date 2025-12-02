import streamlit as st
import openai
import anthropic
import google.generativeai as genai

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Nirmal-Bhasha AI", page_icon="🕉️")

# --- HIDE STREAMLIT BRANDING ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.title("🕉️ Nirmal-Bhasha: Hindi Purity Analyzer")

# --- USER INPUT ---
model_choice = st.selectbox(
    "Choose your Linguist Engine:",
    ["Gemini Pro (Google)", "GPT-4o (OpenAI)", "Claude 3.5 (Anthropic)"]
)

user_text = st.text_area("Enter Hindi text here:", height=150)

# --- THE SYSTEM PROMPT (THIS IS WHAT YOU ASKED ABOUT) ---
# I have pasted your text exactly below inside the quotes """ ... """
system_prompt = """
You are 'Nirmal-Bhasha', an expert Hindi Etymologist. Your task is to analyze the user's text for 'Tatsam' (Sanskrit-root), 'Tadbhav' (Evolved), and 'Videshi' (Foreign) words.

Identify all foreign loanwords (English/Urdu/Persian).
Calculate a 'Purity Percentage' (approximate).
Suggest pure 'Tatsam' alternatives for every foreign word found.
Keep the tone academic but encouraging. Output in clean Markdown.
"""

# --- THE LOGIC ---
def get_analysis(text, model):
    try:
        if "Gemini" in model:
            genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            return model.generate_content(f"{system_prompt}\n\nUser Text: {text}").text
            
        elif "OpenAI" in model:
            client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text}
                ]
            )
            return response.choices[0].message.content
            
        elif "Anthropic" in model:
            client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
            msg = client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=1000,
                system=system_prompt,
                messages=[{"role": "user", "content": text}]
            )
            return msg.content[0].text

    except Exception as e:
        return f"Error: {str(e)}"

if st.button("Analyze Purity"):
    if user_text:
        with st.spinner("Analyzing..."):
            result = get_analysis(user_text, model_choice)
            st.markdown(result)
    else:

        st.warning("Please enter text first.")
# --- DIAGNOSTIC: PASTE AT BOTTOM OF APP.PY ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    st.write("### Available Models for your Key:")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            st.code(m.name)
except Exception as e:
    st.write(f"Key Error: {e}")

