import streamlit as st
from utils import get_ai_response, save_feedback

st.set_page_config(page_title="Nibandh-Lekhan", page_icon="🖋️", layout="centered")

col_logo, col_text = st.columns([1.5, 4.5])
with col_logo: st.markdown("<div style='font-size: 80px; text-align: center;'>🖋️</div>", unsafe_allow_html=True)
with col_text: st.markdown("<div><h1 style='margin: 0;'>Nibandh-Lekhan</h1><p style='margin: 0; color: #666;'>Expert Hindi Essay Architect</p></div>", unsafe_allow_html=True)
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    topic = st.text_input("Essay Topic", placeholder="Ex: Aatmanirbhar Bharat")
    word_limit = st.select_slider("Word Limit", ["Short (250)", "Medium (500)", "Long (800+)"])
with col2:
    level = st.selectbox("Level", ["School (6-10)", "College", "UPSC/Govt"])
    style = st.selectbox("Style", ["Analytical", "Descriptive", "Reflective"])

key_points = st.text_area("Key Points (Optional)")
with st.expander("⚙️ Settings"): model = st.selectbox("AI Model", ["Gemini 2.5 Flash", "Meta Llama 3"])

if "essay_result" not in st.session_state: st.session_state.essay_result = None

if st.button("Compose Essay", type="primary", use_container_width=True):
    if topic:
        sys_prompt = f"You are 'Acharya Nibandh'. Write a Hindi Essay on '{topic}'. Level: {level}, Style: {style}, Length: {word_limit}. STRUCTURE: Prastavana -> Vishay Vastu -> Upsanghar. Language: Shuddh Hindi (No English)."
        with st.spinner("Writing..."):
            st.session_state.essay_result = get_ai_response(sys_prompt, f"Topic: {topic}. Points: {key_points}", model)

if st.session_state.essay_result:
    st.markdown(st.session_state.essay_result)
    st.download_button("📥 Download", st.session_state.essay_result, f"{topic}_Essay.md")
    if st.button("👍 Good Structure?"): save_feedback("Nibandh-Lekhan", topic, st.session_state.essay_result, "Positive")
