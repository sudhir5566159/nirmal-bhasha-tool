import streamlit as st
from utils import show_header, get_ai_response, load_correction_rules

# --- PAGE CONFIG ---
st.set_page_config(page_title="Nirmal-Bhasha", page_icon="🪷")

# 1. SHOW THE MAIN UMBRELLA HEADER (Optional - keeps the ShabdaSankalan link)
show_header()

# 2. SHOW YOUR BRANDING LOGO (Loud and Clear)
# We use columns to center the logo perfectly
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("nirmal_logo.png", use_container_width=True)

# 3. THE TOOL INTERFACE
st.markdown("### 🔍 Purity Analyzer (शुद्धता विश्लेषक)")
model = st.selectbox("Engine:", ["Gemini 2.0 Flash (Google)", "GPT-4o (OpenAI)"])
text = st.text_area("Enter Text:", height=150, placeholder="Example: Meri gaadi kharab ho gayi hai.")

if st.button("Analyze Purity", type="primary"):
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
