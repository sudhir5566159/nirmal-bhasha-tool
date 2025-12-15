import streamlit as st
from utils import get_ai_response, load_correction_rules

# --- PAGE CONFIG ---
st.set_page_config(page_title="Nirmal-Bhasha", page_icon="🪷", layout="centered")

# --- 1. THE "FORTUNE 100" HEADER (Endorsed Brand Style) ---
# We use columns to push the "Umbrella Brand" to the top-right corner
col_blank, col_brand = st.columns([3, 1])

with col_brand:
    # This acts as the "Endorsement Stamp"
    st.markdown("""
        <div style="text-align: right; border-left: 2px solid #ddd; padding-left: 10px;">
            <p style="
                font-size: 10px; 
                text-transform: uppercase; 
                letter-spacing: 2px; 
                color: gray; 
                margin-bottom: 0px;">
                Part of
            </p>
            <p style="
                font-size: 14px; 
                font-weight: 600; 
                color: #444; 
                margin: 0px;">
                ShabdaSankalan AI
            </p>
        </div>
        """, unsafe_allow_html=True)

# --- 2. THE HERO SECTION (Specific App Branding) ---
st.markdown("<br>", unsafe_allow_html=True) # Add a little breathing room

# Center alignment for the Logo and Title using standard CSS margin tricks
col_left, col_center, col_right = st.columns([1, 2, 1])

with col_center:
    # A. The Logo (Large, Clear, Centered)
    st.image("nirmal_logo.png", use_container_width=True)
    
    # B. The Title (Elegant Typography)
    st.markdown("""
        <div style="text-align: center;">
            <h1 style="
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                color: #1E1E1E;
                font-size: 32px;
                margin-top: -10px;
                font-weight: 700;">
                Nirmal Bhasha
            </h1>
            <p style="
                font-size: 16px;
                color: #666;
                font-style: italic;
                margin-top: -5px;">
                The Gold Standard for Hindi Purity
            </p>
        </div>
        """, unsafe_allow_html=True)

# --- 3. THE TOOL INTERFACE ---
st.markdown("---") # Elegant separator line

# Using a card-like background for the inputs (optional visual polish)
model = st.selectbox("Select Intelligence Engine / इंजन चुनें:", ["Gemini 2.0 Flash (Google)", "GPT-4o (OpenAI)"])
text = st.text_area("Input Text / पाठ दर्ज करें:", height=150, placeholder="Type here to analyze... (Example: Meri gaadi kharab ho gayi hai)")

# Action Button
if st.button("Analyze Purity (विश्लेषण करें)", type="primary"):
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
        with st.spinner("Processing with ShabdaSankalan AI..."):
            st.markdown(get_ai_response(sys_prompt, text, model))
