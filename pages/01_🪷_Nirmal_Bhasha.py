import streamlit as st
from utils import get_ai_response, load_correction_rules, save_feedback

# --- PAGE CONFIG ---
st.set_page_config(page_title="Nirmal-Bhasha", page_icon="🌸", layout="centered")

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

# Session State
if "nirmal_result" not in st.session_state:
    st.session_state.nirmal_result = None
if "feedback_submitted" not in st.session_state:
    st.session_state.feedback_submitted = False

# --- ACTION BUTTON ---
if st.button("Analyze Purity / शुद्धता जांचें", type="primary", use_container_width=True):
    st.session_state.feedback_submitted = False
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
    
    st.markdown(st.session_state.nirmal_result)
    
    st.markdown("---")
    
    # 2. IMPACTFUL REALITY CHECK (Bilingual)
    st.warning("""
    #### ⚠️ क्या 2050 तक हिंदी बदल जाएगी? (Will Hindi change forever?)
    
    **सच्चाई (The Reality):**
    विशेषज्ञों का मानना है कि 'हिंदी' अब उतनी हिंदी नहीं रही। यह तेजी से बदल रही है और हमारी बातचीत का कम से कम 40% हिस्सा अब विदेशी है, जिसमें अरबी, फारसी और अंग्रेजी का बड़ा प्रभाव है। ये सभी भाषाएं महान हैं, लेकिन आपकी संस्कृति का हजारों वर्षों से हिस्सा रहे, बचपन में सुने गए कई हिंदी शब्द अब लगभग विलुप्त हो चुके हैं। हिंदी शब्दावली धीरे-धीरे कोमा में जा रही है। हमने इस रुझान को पलटने के लिए यह AI बनाया है।
    *(Experts warn that 'Hindi' is rapidly evolving, with at least 40% of our conversation now consisting of foreign influences like Arabic, Persian, and English. While these languages are great, many traditional Hindi terms—part of our culture for millennia and known from childhood—are becoming extinct. Hindi vocabulary is gradually slipping into a coma. We built this AI to reverse that trend.)*
    
    **पारदर्शिता (Transparency):**
    * **AI Cost for this analysis:** ₹2.00 (Paid by us)
    * **Cost to you:** ₹0.00 (Free)
    
    **If this tool adds value, help us keep the servers running.**
    """)
    
    col_cta1, col_cta2 = st.columns(2)
    
    with col_cta1:
        st.markdown("### 📢 Share the Pride")
        st.caption("Copy this text for WhatsApp:")
        
        share_text = """✅ Hindi Purity Verified (हिंदी शुद्धता सत्यापित)
🛡️ I stand for Pure Hindi.
Today, I took a minute to filter out foreign words.

Status: [Insert Score]% Pure (Shuddh)
Foreign Words Found: [Count]
Verdict: Excellent Standard

Let's stop normalizing Hinglish.
Verify your content here: ShabdaSankalan.com"""
        
        st.text_area("Copy text below:", value=share_text, height=230, label_visibility="collapsed")
        
    with col_cta2:
        st.markdown("### ☕ Fuel the Mission")
        st.caption("Support the team:")
        
        # 3. TWO SUPPORT OPTIONS
        # Razorpay Link (Existing)
        st.markdown(
            f"""
            <a href="https://razorpay.me/@shabdasankalan" target="_blank" style="text-decoration: none;">
                <img src="https://img.shields.io/badge/Support-Buy%20Chai%20%2F%20Coffee-FFDD00?style=for-the-badge&logo=buymeacoffee&logoColor=black" alt="Support via Razorpay" height="45" style="margin-bottom: 10px;" />
            </a>
            """,
            unsafe_allow_html=True
        )
        # Buy Me A Coffee Link (New, using the uploaded image)
        st.markdown(
            f"""
            <a href="https://buymeacoffee.com/shabdasankalan" target="_blank">
                <img src="image_0.png" alt="Buy Me A Coffee" height="45" />
            </a>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")
    col_dl, col_fb = st.columns([1, 1])
    
    with col_dl:
        st.download_button("📄 Download Report", st.session_state.nirmal_result, "Nirmal_Report.md")
        
    with col_fb:
        # 1. ENHANCED FEEDBACK SYSTEM
        st.caption("Rate the analysis:")
        col_f1, col_f2 = st.columns([1, 1])
        with col_f1:
            if st.button("👍 Good", key="good_feedback"):
                save_feedback("Nirmal-Bhasha", text, st.session_state.nirmal_result, "Positive")
                st.toast("Thanks for your positive feedback!")
                st.session_state.feedback_submitted = True
        with col_f2:
            if st.button("👎 Bad", key="bad_feedback"):
                st.session_state.show_negative_feedback = True
        
        if st.session_state.get("show_negative_feedback") and not st.session_state.feedback_submitted:
            with st.form("negative_feedback_form"):
                negative_reason = st.text_input("Please specify the reason (Optional):", placeholder="e.g., Missed a word, incorrect analysis...")
                if st.form_submit_button("Submit Feedback"):
                    save_feedback("Nirmal-Bhasha", text, st.session_state.nirmal_result, "Negative", negative_reason)
                    st.toast("Thanks for your feedback! We'll improve.")
                    st.session_state.feedback_submitted = True
                    st.session_state.show_negative_feedback = False
                    st.rerun()
