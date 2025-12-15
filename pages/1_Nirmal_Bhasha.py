import streamlit as st
from utils import get_ai_response, load_correction_rules

# --- PAGE CONFIG ---
st.set_page_config(page_title="Nirmal-Bhasha", page_icon="🪷", layout="centered")

# --- 1. ENDORSEMENT HEADER ---
col_empty, col_endorser = st.columns([3, 1])
with col_endorser:
    st.markdown("""
        <div style="text-align: right; margin-bottom: 10px;">
            <span style="font-size: 10px; text-transform: uppercase; color: #888; letter-spacing: 1px;">Part of</span>
            <br>
            <span style="font-size: 12px; font-weight: 600; color: #555;">ShabdaSankalan AI</span>
        </div>
        """, unsafe_allow_html=True)

# --- 2. HERO BRANDING ---
col_logo, col_text = st.columns([1.5, 4.5])

with col_logo:
    st.image("nirmal_logo.png", width=120)

with col_text:
    st.markdown("""
        <div style="padding-top: 10px;">
            <h1 style="
                margin: 0;
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                font-size: 34px;
                font-weight: 700;
                color: #1E1E1E;
                line-height: 1.2;">
                Nirmal Bhasha
            </h1>
            <p style="
                margin: 0;
                font-size: 16px;
                color: #666;
                font-weight: 400;">
                The Gold Standard for Hindi Purity
            </p>
        </div>
        """, unsafe_allow_html=True)

# --- 3. THE TOOL INTERFACE ---
st.markdown("---") 

# Tool Controls
col_input, col_settings = st.columns([3, 1])

with col_settings:
    model = st.selectbox(
        "Engine / इंजन:", 
        ["Gemini 2.5 Flash (Google)", "Meta Llama 3 (via Groq)", "Claude 3.5 Sonnet (Anthropic)"], 
        label_visibility="collapsed"
    )

with col_input:
    st.caption("Select Engine above | Enter text below (इंजन चुनें | पाठ दर्ज करें):")

text = st.text_area(
    "Input Text", 
    height=150, 
    placeholder="Start typing here... \nयहाँ टाइप करना शुरू करें... \n(Example: Meri gaadi kharab hai)", 
    label_visibility="collapsed"
)

# Action Button
if st.button("Analyze Purity / शुद्धता जांचें", type="primary", use_container_width=True):
    rules = load_correction_rules()
    
    # --- THE "STUNNING" PROMPT ---
    # We explicitly tell the AI to format the top section with Emojis, Tables, and Progress Bars.
    sys_prompt = f"""
    You are 'Nirmal-Bhasha' (निर्मल-भाषा), the most advanced Hindi Purity Analyzer.
    
    YOUR GOAL: Analyze the input text for foreign words (Urdu, English, Persian, Arabic) and provide a corrected Pure Hindi version.
    
    OUTPUT FORMAT REQUIREMENTS (STRICT):
    1. Start with a **"Visual Dashboard"** using Markdown tables and large emojis.
    2. Use a **"Visual Progress Bar"** for the score (e.g., 🟩🟩🟩🟩⬜ 80%).
    3. Then provide the **Detailed Analysis** (the text analysis you usually do).
    4. Finally, provide the **Refined Sentence**.

    CRITICAL CORRECTION RULES (Apply these fixes):
    {rules}

    ---
    EXPECTED OUTPUT STRUCTURE (Copy this style):

    # 🕉️ निर्मल-भाषा विश्लेषण रिपोर्ट (Nirmal-Bhasha Report)

    ### 📊 शुद्धता स्कोर (Purity Score)
    > **95.21%** 🟩🟩🟩🟩🟩🟩🟩🟩🟩⬜ (Excellent)

    | 📜 कुल शब्द (Total) | 🚫 विदेशी शब्द (Foreign) | ✅ शुद्ध शब्द (Pure) |
    | :---: | :---: | :---: |
    | **146** | **7** | **139** |

    ---

    ### 🔍 विस्तृत विश्लेषण (Detailed Analysis)
    (Provide your detailed word-by-word analysis here as you usually do...)

    ### 🛠️ शब्द सुधार (Word Correction)
    | ❌ अशुद्ध/विदेशी | 🌍 मूल (Origin) | ✅ शुद्ध हिन्दी (Correction) |
    | :--- | :--- | :--- |
    | (Fill this table...) | ... | ... |

    ### ✨ परिशोधित वाक्य (Refined Sentence)
    > (Write the final pure Hindi paragraph here...)
    
    ---
    """
    
    if text:
        with st.spinner("Processing... (प्रक्रिया जारी है...)"):
            st.markdown(get_ai_response(sys_prompt, text, model))
