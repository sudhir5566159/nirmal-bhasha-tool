import streamlit as st
from utils import get_ai_response, load_correction_rules

# --- PAGE CONFIG ---
st.set_page_config(page_title="Nirmal-Bhasha", page_icon="🪷", layout="centered")

# --- 1. ENDORSEMENT HEADER (Subtle Top-Right) ---
col_empty, col_endorser = st.columns([3, 1])
with col_endorser:
    st.markdown("""
        <div style="text-align: right; margin-bottom: 10px;">
            <span style="font-size: 10px; text-transform: uppercase; color: #888; letter-spacing: 1px;">Part of</span>
            <br>
            <span style="font-size: 12px; font-weight: 600; color: #555;">ShabdaSankalan AI</span>
        </div>
        """, unsafe_allow_html=True)

# --- 2. HERO BRANDING (Horizontal Lockup) ---
# Adjusted columns to fit the larger logo
col_logo, col_text = st.columns([1.5, 4.5])

with col_logo:
    # INCREASED SIZE: 120px makes the tagline readable
    st.image("nirmal_logo.png", width=120)

with col_text:
    # Text aligned to the larger logo
    st.markdown("""
        <div style="padding-top: 10px;">
            <h1 style="
                margin: 0;
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                font-size: 34px;
                font-weight: 700;
                color: #1E1E1E;
                line-height: 1.2;">
                Nirmal Bhasha
            </h1>
            <p style="
                margin: 0;
                font-size: 16px;
                color: #666;
                font-weight: 400;">
                The Gold Standard for Hindi Purity
            </p>
        </div>
        """, unsafe_allow_html=True)

# --- 3. THE TOOL INTERFACE ---
st.markdown("---") # Thin divider line

# Tool Controls
col_input, col_settings = st.columns([3, 1])

with col_settings:
    model = st.selectbox("Engine:", ["Gemini 2.0 Flash (Google)", "Meta Llama 3 (via Groq)"], label_visibility="collapsed")

with col_input:
    # ADDED HINDI INSTRUCTION
    st.caption("Select Engine above | Enter text below (इंजन चुनें | पाठ दर्ज करें):")

# ADDED HINDI PLACEHOLDER
text = st.text_area(
    "Input Text", 
    height=150, 
    placeholder="Start typing here... \nयहाँ टाइप करना शुरू करें... \n(Example: Meri gaadi kharab hai)", 
    label_visibility="collapsed"
)

# Action Button
if st.button("Analyze Purity / शुद्धता जांचें", type="primary", use_container_width=True):
    rules = load_correction_rules()
    sys_prompt = f"""
    You are 'Nirmal-Bhasha' (निर्मल-भाषा). 
    RULES: Output MUST be in Devanagari Hindi.
    Calculate Purity Score. Identify Foreign words.
    CRITICAL CORRECTION LIST:
    {rules}
    Structure response with 'Purity Analysis', 'Word Correction' (Table), and 'Refined Sentence'.
    """
    if text:
        with st.spinner("Processing... (प्रक्रिया जारी है...)"):
            st.markdown(get_ai_response(sys_prompt, text, model))
