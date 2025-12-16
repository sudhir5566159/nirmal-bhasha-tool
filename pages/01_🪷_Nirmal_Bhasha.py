import streamlit as st
from utils import get_ai_response, load_correction_rules, save_feedback

# --- PAGE CONFIG ---
# We use the Lotus emoji here. If it looks like a box to you, don't worry.
st.set_page_config(page_title="Nirmal-Bhasha", page_icon="🪷", layout="centered")

# --- HEADER ---
col_empty, col_endorser = st.columns([3, 1])
with col_endorser:
    st.markdown("""
        <div style="text-align: right; margin-bottom: 10px;">
            <span style="font-size: 10px; text-transform: uppercase; color: #888; letter-spacing: 1px;">Part of</span>
            <br>
            <span style="font-size: 12px; font-weight: 600; color: #555;">ShabdaSankalan AI</span>
        </div>
        """, unsafe_allow_html=True)

col_logo, col_text = st.columns([1.5, 4.5])
with col_logo:
    # FORCE THE LOTUS SYMBOL (Encoded for safety)
    # This guarantees the Lotus appears even if your file name looks like a box
    st.markdown("<div style='font-size: 80px; text-align: center;'>🪷</div>", unsafe_allow_html=True)

with col_text:
    st.markdown("""
        <div style="padding-top: 10px;">
            <h1 style="margin: 0; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 34px; font-weight: 700; color: #1E1E1E; line-height: 1.2;">Nirmal Bhasha</h1>
            <p style="margin: 0; font-size: 16px; color: #666; font-weight: 400;">The Gold Standard for Hindi Purity</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---") 

# --- INPUT SECTION ---
col_input, col_settings = st.columns([3, 1])
with col_settings:
    model = st.selectbox("Engine / इंजन:", ["Gemini 2.5 Flash (Google)", "Meta Llama 3 (via Groq)", "Claude 3.5 Sonnet (Anthropic)"], label_visibility="collapsed")
with col_input:
    st.caption("Select Engine above | Enter text below (इंजन चुनें | पाठ दर्ज करें):")

text = st.text_area("Input Text", height=150, placeholder="Start typing here... \n(Example: Meri gaadi kharab hai)", label_visibility="collapsed")

# Session State
if "nirmal_result" not in st.session_state:
    st.session_state.nirmal_result = None

# --- ACTION BUTTON ---
if st.button("Analyze Purity / शुद्धता जांचें", type="primary", use_container_width=True):
    rules = load_correction_rules()
    
    # SYSTEM PROMPT
    sys_prompt = f"""
    You are 'Nirmal-Bhasha'. Analyze for Foreign words (Urdu, English, Persian).
    CRITICAL CORRECTION LIST: {rules}
    
    OUTPUT FORMAT REQUIREMENTS:
    1. Start with a **"Visual Dashboard"** (Markdown tables).
    2. Use a **"Visual Progress Bar"** for score (e.g. 🟩🟩🟩⬜ 80%).
    3. Detailed Analysis & Word Correction Table.
    4. Refined Sentence.
    """
    
    if text:
        with st.spinner("Processing... (प्रक्रिया जारी है...)"):
            final_report = get_ai_response(sys_prompt, text, model)
            st.session_state.nirmal_result = final_report

# --- RESULT DISPLAY ---
if st.session_state.nirmal_result:
    
    # 1. THE REPORT
    st.markdown(st.session_state.nirmal_result)
    
    st.markdown("---")
    
    # 2. THE REALITY CHECK
    st.warning("""
    #### ⚠️ क्या 2050 तक हिंदी बदल जाएगी? (Will Hindi change forever?)
    **The Reality:** Experts warn that "Hinglish" is rapidly replacing our vocabulary. 40% of urban speech is now foreign. We built this AI to reverse that trend.
    
    **Transparency:**
    * **AI Cost for this analysis:** ₹2.00 (Paid by us)
    * **Cost to you:** ₹0.00 (Free)
    
    If this tool adds value, help us keep the servers running.
    """)
    
    col_cta1, col_cta2 = st.columns(2)
    
    with col_cta1:
        # 3. SHARE TEXT
        st.markdown("### 📢 Share the Pride")
        st.caption("Copy this text for WhatsApp:")
        
        share_text = """✅ Hindi Purity Verified (हिंदी शुद्धता सत्यापित)
🛡️ I stand for Pure Hindi.
Today, I took a minute to filter out foreign words from my communication.

Status: [Insert Score]% Pure (Shuddh)
Foreign Words Found: [Count]
Verdict: Excellent Standard

Let's stop normalizing Hinglish. Small steps save a language. 
Verify your content here: ShabdaSankalan.com"""
        
        st.code(share_text, language="text")
        
    with col_cta2:
        # 4. SUPPORT (Reciprocity)
        st.markdown("### ☕ Fuel the Mission")
        st.caption("Keep this tool free for students.")
        st.markdown("[![Support via UPI](https://img.shields.io/badge/Support-₹20_Chai-orange?style=for-the-badge&logo=bhim)](https://www.google.com)")

    # 5. DOWNLOAD & FEEDBACK
    st.markdown("---")
    col_dl, col_fb = st.columns([1, 1])
    
    with col_dl:
        st.download_button("📄 Download Report", st.session_state.nirmal_result, "Nirmal_Report.md")
        
    with col_fb:
        if st.button("👍 Correct Analysis?"):
            save_feedback("Nirmal-Bhasha", text, st.session_state.nirmal_result, "Positive")
            st.toast("Thanks for verifying!")
