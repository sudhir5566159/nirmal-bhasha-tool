import streamlit as st
from utils import show_header, get_ai_response, load_correction_rules

# --- PAGE CONFIG ---
st.set_page_config(page_title="Nirmal-Bhasha", page_icon="🪷")

# 1. SHOW MAIN UMBRELLA HEADER (The "ShabdaSankalan" top bar)
show_header()

# 2. COMPACT TOOL HEADER (Logo + Text Side-by-Side)
# We make two columns: A small one for the logo, a wider one for the text
col_logo, col_text = st.columns([1, 4])

with col_logo:
    # We restrict the width to 90 pixels so it stays sharp and small
    st.image("nirmal_logo.png", width=90)

with col_text:
    # We use Custom HTML to align the text perfectly with the logo
    st.markdown("""
        <div style="padding-top: 10px;">
            <h2 style="margin: 0; color: #333;">Nirmal-Bhasha (निर्मल-भाषा)</h2>
            <p style="margin: 0; color: gray; font-size: 14px;">Pure Language Analysis Tool</p>
        </div>
        """, unsafe_allow_html=True)

# 3. TOOL INTERFACE
st.markdown("---")
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
