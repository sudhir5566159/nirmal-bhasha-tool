import streamlit as st
from utils import get_ai_response, load_correction_rules, save_feedback

# --- PAGE CONFIG ---
st.set_page_config(page_title="Bhasha-Vivek", page_icon="🦢", layout="centered")

# --- HEADER ---
col_logo, col_text = st.columns([1.5, 4.5])
with col_logo: 
    # UPDATED: Swan (Hamsa) represents 'Vivek' (Discernment)
    st.markdown("<div style='font-size: 80px; text-align: center;'>🦢</div>", unsafe_allow_html=True)
with col_text: 
    st.markdown("<div><h1 style='margin: 0;'>Bhasha-Vivek</h1><p style='margin: 0; color: #666;'>Universal Translator to Pure & Practical Hindi</p></div>", unsafe_allow_html=True)
st.markdown("---")

col_input, col_settings = st.columns([3, 1])
with col_settings: model = st.selectbox("Engine", ["Gemini 2.5 Flash", "Meta Llama 3"], label_visibility="collapsed")
with col_input: st.caption("Select Engine | Enter text in ANY language:")
text = st.text_area("Input Text", height=150, placeholder="English, Hinglish, Tamil, French...", label_visibility="collapsed")

if "bhasha_result" not in st.session_state: st.session_state.bhasha_result = None

if st.button("Translate & Refine", type="primary", use_container_width=True):
    rules = load_correction_rules()
    sys_prompt = f"You are 'Bhasha-Vivek'. Translate to Pure & Practical Hindi. GOLDEN RULE: No Urdu/English words, but keep it flowing. CRITICAL RULES: {rules}"
    if text:
        with st.spinner("Translating..."):
            st.session_state.bhasha_result = get_ai_response(sys_prompt, text, model)

if st.session_state.bhasha_result:
    st.markdown(st.session_state.bhasha_result)
    st.download_button("📄 Download", st.session_state.bhasha_result, "Bhasha_Output.md")
    st.markdown("### 🗳️ Rate Quality")
    with st.form("feedback_form"):
        rating = st.radio("How was the translation?", ["🤩 Amazing", "🙂 Excellent", "😐 Average", "😞 Bad"], horizontal=True)
        comments = st.text_input("Comments (Optional)")
        if st.form_submit_button("Submit"):
            save_feedback("Bhasha-Vivek", text, st.session_state.bhasha_result, rating, comments)
            st.success("Recorded!")
