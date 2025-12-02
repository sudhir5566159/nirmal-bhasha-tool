import streamlit as st
import google.generativeai as genai
import openai
import anthropic
import json # Added to read your new database file

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ShabdaSankalan AI Suite",
    page_icon="🪷",
    layout="centered"
)

# --- CSS FOR "WHITE LABEL" LOOK ---
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stTextArea textarea {font-size: 18px !important;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- LOAD CORRECTION RULES FROM JSON ---
def load_correction_rules():
    try:
        with open('corrections.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Convert JSON data into a string list for the AI Prompt
            rules_text = ""
            for rule in data['correction_rules']:
                rules_text += f"- If you see '{rule['word']}', Origin is {rule['origin']}. Replacement: '{rule['replacement']}'.\n"
            return rules_text
    except FileNotFoundError:
        # Fallback if file is missing
        return "- No specific manual corrections loaded."

# Load the rules into a variable
correction_database = load_correction_rules()

# --- THE LOGO SECTION ---
col1, col2 = st.columns([1, 5])
with col1:
    st.markdown("""
        <div style="display: flex; justify-content: center;">
            <svg width="80" height="80" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                <path d="M50 10 C50 10 30 40 10 50 C30 60 50 90 50 90 C50 90 70 60 90 50 C70 40 50 10 50 10 Z" fill="#E91E63" stroke="#C2185B" stroke-width="2"/>
                <circle cx="50" cy="50" r="5" fill="#FFC107" />
                <path d="M50 90 Q30 80 20 60 M50 90 Q70 80 80 60" stroke="#4CAF50" stroke-width="3" fill="none"/>
            </svg>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.title("ShabdaSankalan AI")
    st.caption("The Digital Infrastructure for Hindi Language")

# --- SIDEBAR MENU ---
st.sidebar.header("🧰 AI Tools Menu")
tool_choice = st.sidebar.radio(
    "Select a Tool / उपकरण चुनें:",
    ["🕉️ Nirmal-Bhasha (Purity Check)", 
     "📝 Patra-Lekhak (Letter Writer)",
     "🧪 Bhasha-Vivek (Hinglish to Hindi)"]
)
st.sidebar.markdown("---")
st.sidebar.info("Powered by **ShabdaSankalan.com**")

# --- SHARED API FUNCTION ---
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

# ==========================================
# TOOL 1: NIRMAL BHASHA (PURITY CHECKER)
# ==========================================
if tool_choice == "🕉️ Nirmal-Bhasha (Purity Check)":
    st.subheader("🕉️ Nirmal-Bhasha: Purity Analyzer")
    st.markdown("Check the 'Shuddhata' (Purity) of your Hindi text.")
    
    model = st.selectbox("Engine:", ["Gemini 2.0 Flash (Google)", "GPT-4o (OpenAI)"], key="nirmal_model")
    text = st.text_area("Enter Text:", height=150, placeholder="Example: Meri gaadi kharab ho gayi hai.")
    
    if st.button("Analyze Purity", type="primary"):
        # We inject the 'correction_database' string into the prompt here
        sys_prompt = f"""
        You are 'Nirmal-Bhasha' (निर्मल-भाषा), a strict Hindi Etymologist.
        
        RULES:
        1. YOUR OUTPUT MUST BE IN DEVANAGARI SCRIPT HINDI.
        2. Calculate a 'Purity Score' (shuddhata pratishat).
        3. Identify 'Videshi' (Foreign) words and provide 'Tatsam' (Sanskrit-root) alternatives.
        
        CRITICAL CORRECTION LIST (Follow these strictly to avoid errors):
        {correction_database}

        Structure your response like this:
        ### 📊 शुद्धता विश्लेषण (Purity Analysis)
        **शुद्धता स्कोर:** [Score]%
        
        ### 🔍 शब्द सुधार (Word Correction)
        | अशुद्ध/विदेशी शब्द | शुद्ध विकल्प (Tatsam) | मूल (Origin) |
        | :--- | :--- | :--- |
        | [Word] | [Replacement] | [Origin] |
        
        ### ✨ परिष्कृत वाक्य (Refined Sentence)
        "[Rewritten Sentence in Standard Hindi]"
        """
        
        if text:
            with st.spinner("Consulting linguistic archives..."):
                st.markdown(get_ai_response(sys_prompt, text, model))
        else:
            st.warning("Please enter some text first.")

# ==========================================
# TOOL 2: PATRA-LEKHAK
# ==========================================
elif tool_choice == "📝 Patra-Lekhak (Letter Writer)":
    st.subheader("📝 Patra-Lekhak: Formal Drafter")
    st.markdown("Generate official Hindi letters instantly.")
    model = st.selectbox("Engine:", ["Gemini 2.0 Flash (Google)", "GPT-4o (OpenAI)"], key="patra_model")
    col_a, col_b = st.columns(2)
    with col_a:
        recipient = st.text_input("To whom?", placeholder="Bank Manager")
    with col_b:
        sender_name = st.text_input("Your Name", placeholder="Ramesh Kumar")
    topic = st.text_input("Reason?", placeholder="Account unfreeze karne ke liye")
    
    if st.button("Draft Letter", type="primary"):
        sys_prompt = """
        You are an expert Hindi Secretary. Write a formal, high-quality Hindi application letter.
        - Use standard formal format (Sewa Mein, Vishay, Mahoday).
        - Use strictly formal Hindi vocabulary (Prarthna Patra, Nivedan, etc).
        - Output in clear Devanagari Hindi.
        """
        user_input = f"Write a letter to {recipient} from {sender_name} about: {topic}"
        if topic:
            with st.spinner("Drafting letter..."):
                st.markdown(get_ai_response(sys_prompt, user_input, model))
        else:
            st.warning("Please enter a topic.")

# ==========================================
# TOOL 3: BHASHA-VIVEK
# ==========================================
elif tool_choice == "🧪 Bhasha-Vivek (Hinglish to Hindi)":
    st.subheader("🧪 Bhasha-Vivek: Correction Engine")
    st.markdown("Convert Hinglish to Standard Hindi.")
    model = st.selectbox("Engine:", ["Gemini 2.0 Flash (Google)", "GPT-4o (OpenAI)"], key="vivek_model")
    text = st.text_area("Enter Hinglish Text:", height=150, placeholder="Meeting attend karna important hai.")
    
    if st.button("Convert to Hindi", type="primary"):
        sys_prompt = "Convert the user's Hinglish text into grammatically perfect, formal Standard Hindi (Devanagari). Only output the Hindi translation."
        if text:
            with st.spinner("Converting..."):
                st.markdown(get_ai_response(sys_prompt, text, model))
        else:
            st.warning("Please enter some text.")
