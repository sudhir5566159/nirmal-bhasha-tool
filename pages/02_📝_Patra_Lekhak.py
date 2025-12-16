import streamlit as st
from utils import get_ai_response, save_feedback

st.set_page_config(page_title="Patra-Lekhak", page_icon="📝", layout="centered")

col_logo, col_text = st.columns([1.5, 4.5])
with col_logo: st.markdown("<div style='font-size: 80px; text-align: center;'>📝</div>", unsafe_allow_html=True)
with col_text: st.markdown("<div><h1 style='margin: 0;'>Patra-Lekhak</h1><p style='margin: 0; color: #666;'>Professional Hindi Letter Drafter</p></div>", unsafe_allow_html=True)
st.markdown("---")

st.caption("Fill the details below to generate a formal letter instantly.")
col1, col2 = st.columns(2)
with col1:
    recipient = st.selectbox("To Whom?", ["Principal", "Bank Manager", "Editor", "Police Officer", "Government Official", "Other"])
    sender_name = st.text_input("Your Name", placeholder="Ex: Rahul Sharma")
with col2:
    letter_type = st.selectbox("Letter Type", ["Request", "Complaint", "Appreciation", "Leave Application", "Inquiry"])
    date_option = st.date_input("Date")

topic = st.text_input("Subject/Topic", placeholder="Ex: Request for 2 days leave...")
with st.expander("⚙️ Settings"): model = st.selectbox("AI Model", ["Gemini 2.5 Flash", "Meta Llama 3"])

if "letter_result" not in st.session_state: st.session_state.letter_result = None

if st.button("Draft Letter / पत्र लिखें", type="primary", use_container_width=True):
    if topic and sender_name:
        sys_prompt = f"Write a formal Hindi letter. Recipient: {recipient}, Type: {letter_type}, Subject: {topic}, Sender: {sender_name}, Date: {date_option}. RULES: Perfect Formal Hindi (Seva Mein format)."
        with st.spinner("Drafting..."):
            st.session_state.letter_result = get_ai_response(sys_prompt, f"Write about: {topic}", model)

if st.session_state.letter_result:
    st.markdown("### 📄 Drafted Letter")
    st.text_area("Copy text:", value=st.session_state.letter_result, height=400)
    st.download_button("📥 Download", st.session_state.letter_result, "Hindi_Letter.txt")
    if st.button("👍 Good Draft?"): save_feedback("Patra-Lekhak", topic, st.session_state.letter_result, "Positive")
