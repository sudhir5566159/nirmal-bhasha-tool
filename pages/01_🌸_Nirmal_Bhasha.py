import streamlit as st
import base64
from utils import get_ai_response, load_correction_rules, save_feedback

# --- PAGE CONFIG ---
st.set_page_config(page_title="Nirmal-Bhasha", page_icon="🌸", layout="centered")

# --- HELPER: IMAGE TO BASE64 ---
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

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
    try:
        st.image("nirmal_logo.png", width=120)
    except:
        st.markdown("<div style='font-size: 80px; text-align: center;'>🌸</div>", unsafe_allow_html=True)

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

# --- SESSION STATE MANAGEMENT ---
if "nirmal_result" not in st.session_state:
    st.session_state.nirmal_result = None
if "analyzed_text" not in st.session_state:
    st.session_state.analyzed_text = ""  # New: To lock the input text
if "feedback_submitted" not in st.session_state:
    st.session_state.feedback_submitted = False
if "show_negative_box" not in st.session_state:
    st.session_state.show_negative_box = False

# --- ACTION BUTTON ---
if st.button("Analyze Purity / शुद्धता जांचें", type="primary", use_container_width=True):
    # Reset Feedback states
    st.session_state.feedback_submitted = False
    st.session_state.show_negative_box = False
    
    # Lock the input text into session state so feedback is accurate
    st.session_state.analyzed_text = text
    
    rules = load_correction_rules()
    
    sys_prompt = f"""
    You are 'Nirmal-Bhasha'. Analyze for Foreign words (Urdu, English, Persian).
    CRITICAL CORRECTION LIST: {rules}
    
    OUTPUT FORMAT REQUIREMENTS:
    1. **The 'Wow' Factor:** Start immediately with a Visual Scorecard. Use a Markdown Table.
       - Columns: '🏆 Purity Score', '🚩 Foreign Words', '✨ Verdict'.
       - Make the verdict encouraging (e.g., "Excellent Effort", "Good Start").
    2. **Visual Progress:** Show a progress bar (e.g., 🟩🟩🟩🟩⬜ 80%).
    3. **The Details:** Detailed Analysis & Word Correction Table.
    4. **The Fix:** Refined Sentence (Pure Hindi).
    """
    
    if text:
        with st.spinner("Processing... (प्रक्रिया जारी है...)"):
            final_report = get_ai_response(sys_prompt, text, model)
            st.session_state.nirmal_result = final_report

# --- RESULT DISPLAY ---
if st.session_state.nirmal_result:
    
    # 1. THE MAIN RESULT (Always Visible)
    st.markdown(st.session_state.nirmal_result)
    st.markdown("---")

    # 2. FEEDBACK & DOWNLOAD (Always Visible - Outside Expander)
    # We use 'analyzed_text' here to ensure we save exactly what was checked.
    col_dl, col_fb = st.columns([1, 1.5])
    
    with col_dl:
        st.download_button("📄 Download Report", st.session_state.nirmal_result, "Nirmal_Report.md")
        
    with col_fb:
        if not st.session_state.feedback_submitted:
            col_f1, col_f2 = st.columns([1, 1])
            with col_f1:
                if st.button("👍 Good"):
                    # SAVE: Locked Input + Current Output
                    save_feedback("Nirmal-Bhasha", st.session_state.analyzed_text, st.session_state.nirmal_result, "Positive")
                    st.toast("Thanks! We are glad it helped.")
                    st.session_state.feedback_submitted = True
                    st.rerun()
            with col_f2:
                if st.button("👎 Bad"):
                    st.session_state.show_negative_box = True
    
    # Negative Feedback Form (Conditional)
    if st.session_state.show_negative_box and not st.session_state.feedback_submitted:
        with st.form("neg_feedback"):
            reason = st.text_input("What went wrong?", placeholder="e.g. Missed a word...")
            if st.form_submit_button("Submit Issue"):
                # SAVE: Locked Input + Current Output + Reason
                save_feedback("Nirmal-Bhasha", st.session_state.analyzed_text, st.session_state.nirmal_result, "Negative", reason)
                st.success("Thanks. We will fix this!")
                st.session_state.feedback_submitted = True
                st.session_state.show_negative_box = False
                st.rerun()

    if st.session_state.feedback_submitted:
        st.success("Feedback Recorded. Thank you!")
    
    st.markdown("---")

    # 3. THE "HEAVY" CONTENT (Hidden in Expander for Lightness)
    with st.expander("ℹ️ ⚠️ The Reality & Support (सच्चाई और सहयोग) - Tap to Open"):
        
        st.warning("""
        #### ⚠️ क्या 2050 तक हिंदी बदल जाएगी? (Will Hindi change forever?)
        
        **सच्चाई (The Reality):**
        विशेषज्ञ चेतावनी देते हैं कि 'हिंदी' अब उतनी हिंदी नहीं रही। यह तेजी से बदल रही है और हमारी बातचीत का कम से कम 40% हिस्सा अब विदेशी है।
        
        आपकी संस्कृति का हजारों वर्षों से हिस्सा रहे, बचपन में सुने गए कई हिंदी शब्द अब लगभग विलुप्त हो चुके हैं। **हिंदी शब्दावली धीरे-धीरे कोमा में जा रही है (Hindi vocabulary is gradually going into a coma).** हमने इस रुझान को पलटने के लिए यह AI बनाया है।
        
        **पारदर्शिता (Transparency):**
        * **AI Cost for this analysis:** ₹2.00 (Paid by us)
        * **Cost to you:** ₹0.00 (Free)
        """)
        
        col_cta1, col_cta2 = st.columns(2)
        
        with col_cta1:
            st.markdown("### 📢 Share")
            share_text = """✅ Hindi Purity Verified (हिंदी शुद्धता सत्यापित)
🛡️ I stand for Pure Hindi.
Status: [Insert Score]% Pure (Shuddh)
Verdict: Excellent Standard
Let's stop normalizing Hinglish.
Verify: ShabdaSankalan.com"""
            st.text_area("Copy:", value=share_text, height=150, label_visibility="collapsed")
            
        with col_cta2:
            st.markdown("### ☕ Support")
            
            # Razorpay
            st.markdown(
                f"""
                <a href="https://razorpay.me/@shabdasankalan" target="_blank" style="text-decoration:none;">
                    <img src="https://img.shields.io/badge/Support-₹_Chai_%2F_Coffee-FFDD00?style=for-the-badge&logo=razorpay&logoColor=black" alt="Support via Razorpay" height="42" />
                </a>
                <div style="margin-bottom: 12px;"></div>
                """,
                unsafe_allow_html=True
            )
            
            # Buy Me A Coffee (Base64)
            bmc_img_base64 = get_base64_image("greeen-button.png")
            if bmc_img_base64:
                st.markdown(
                    f"""
                    <a href="https://buymeacoffee.com/shabdasankalan" target="_blank">
                        <img src="data:image/png;base64,{bmc_img_base64}" width="150" alt="Buy Me A Coffee" />
                    </a>
                    """,
                    unsafe_allow_html=True
                )
            else:
                 st.markdown("[☕ Buy Me A Coffee](https://buymeacoffee.com/shabdasankalan)")
