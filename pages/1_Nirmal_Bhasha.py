import streamlit as st
from utils import show_header, get_ai_response, load_correction_rules

# --- PAGE CONFIG ---
st.set_page_config(page_title="Nirmal-Bhasha", page_icon="🪷")

# 1. TOP HEADER (ShabdaSankalan Umbrella)
show_header()

# 2. BRANDING SECTION (Logo + Hindi Name)
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Display the Logo Image
    st.image("nirmal_logo.png", use_container_width=True)
    
    # Display the Name in Hindi (Centered & Bold)
    st.markdown("""
        <h2 style='text-align: center; color: #333;'>
            निर्मल-भाषा
        </h2>
        <p style='text-align: center; color: gray; margin-top: -10px;'>
            Pure Language Analysis
        </p>
        """, unsafe_allow_html=True)

# 3. TOOL INTERFACE
st.markdown("---") # A light line separator
model = st.selectbox("Engine / इंजन:", ["Gemini 2.0 Flash (Google)", "GPT-4o (OpenAI)"])
text = st.text_area("Enter Text / पाठ दर्ज करें:", height=150, placeholder="Example: Meri gaadi kharab ho gayi hai.")

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
        with st.spinner("Analyzing..."):
            st.markdown(get_ai_response(sys_prompt, text, model))
