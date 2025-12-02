import streamlit as st
import google.generativeai as genai
import openai
import anthropic

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Nirmal-Bhasha AI",
    page_icon="🕉️",
    layout="centered"
)

# --- CSS FOR "WHITE LABEL" LOOK ---
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stTextArea textarea {font-size: 18px !important;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- 1. THE UI LAYOUT ---
st.title("🕉️ Nirmal-Bhasha: Hindi Purity Analyzer")
st.markdown("### Check the 'Shuddhata' (Purity) of your Hindi text.")

# Dropdown for Model Selection
model_choice = st.selectbox(
    "Choose your Linguist Engine / विशेषज्ञ चुनें:",
    ["Gemini 2.0 Flash (Google) - Free/Fast", 
     "GPT-4o (OpenAI) - Most Precise", 
     "Claude 3.5 Sonnet (Anthropic) - Best for Literature"]
)

# Text Input Area
user_text = st.text_area(
    "Enter text here / अपना पाठ यहाँ लिखें:",
    height=200,
    placeholder="Example: Main aaj market gaya tha aur wahan se vegetables khareeda."
)

# --- 2. THE LOGIC FUNCTION ---
def get_purity_analysis(text, model_name):
    # The Secret System Prompt
    system_prompt = """
    You are 'Nirmal-Bhasha' (निर्मल-भाषा), a strict Hindi Etymologist.
    
    RULES:
    1. YOUR OUTPUT MUST BE IN DEVANAGARI SCRIPT HINDI (except for specific English terms being analyzed). Do not use Roman Hindi (Hinglish).
    2. Calculate a 'Purity Score' (shuddhata pratishat).
    3. Identify 'Videshi' (Foreign) words and provide 'Tatsam' (Sanskrit-root) alternatives.
    4. Rewrite the input sentence in high-level, formal Standard Hindi.
    5. Use Markdown tables for the word list.
    
    Structure your response like this:
    ### 📊 शुद्धता विश्लेषण (Purity Analysis)
    **शुद्धता स्कोर:** [Score]%
    
    ### 🔍 शब्द सुधार (Word Correction)
    | अशुद्ध/विदेशी शब्द | शुद्ध विकल्प | मूल (Origin) |
    | :--- | :--- | :--- |
    | [Word] | [Replacement] | [Origin] |
    
    ### ✨ परिष्कृत वाक्य (Refined Sentence)
    "[Rewritten Sentence]"
    """

    try:
        # LOGIC FOR GOOGLE GEMINI (UPDATED TO 2.0)
        if "Gemini" in model_name:
            # We use the key from your secrets file
            genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
            
            # UPDATED MODEL NAME BASED ON YOUR DIAGNOSTIC
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            combined_prompt = f"{system_prompt}\n\nUser Text: {text}"
            response = model.generate_content(combined_prompt)
            return response.text

        # LOGIC FOR OPENAI (GPT-4)
        elif "OpenAI" in model_name:
            client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text}
                ]
            )
            return response.choices[0].message.content

        # LOGIC FOR ANTHROPIC (CLAUDE)
        elif "Anthropic" in model_name:
            client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
            message = client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=1000,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": text}
                ]
            )
            return message.content[0].text

    except Exception as e:
        return f"Error connecting to AI: {str(e)}"

# --- 3. THE EXECUTION ---
if st.button("Analyze Purity / विश्लेषण करें", type="primary"):
    if user_text:
        with st.spinner("Consulting the linguistic archives..."):
            result = get_purity_analysis(user_text, model_choice)
            st.markdown("---")
            st.markdown(result)
    else:
        st.warning("Please enter some Hindi text first.")

