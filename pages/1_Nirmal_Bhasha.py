import streamlit as st
from utils import show_header, get_ai_response, load_correction_rules

# --- PAGE CONFIG ---
st.set_page_config(page_title="Nirmal-Bhasha", page_icon="🪷")

show_header()

st.subheader("🪷 Nirmal-Bhasha: Purity Analyzer")
model = st.selectbox("Engine:", ["Gemini 2.0 Flash (Google)", "GPT-4o (OpenAI)"])
text = st.text_area("Enter Text:", height=150)

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
