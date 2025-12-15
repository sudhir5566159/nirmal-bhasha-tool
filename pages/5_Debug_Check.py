import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Debug Google Models", page_icon="🛠️")

st.title("🛠️ Google Model Scanner")
st.write("This tool checks exactly which models your API Key can access.")

# 1. Configure
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    st.success("✅ API Key Found")
except Exception as e:
    st.error(f"❌ API Key Error: {e}")

# 2. Scan for Models
if st.button("Scan Available Models"):
    try:
        st.write("### 📋 List of Available Models:")
        found_any = False
        
        # Ask Google for the list
        for m in genai.list_models():
            # We only want models that generate text (content)
            if 'generateContent' in m.supported_generation_methods:
                st.code(m.name) # This prints the exact ID like 'models/gemini-pro'
                found_any = True
        
        if not found_any:
            st.warning("No text generation models found. Check your API Key permissions.")
            
    except Exception as e:
        st.error(f"Scan Failed: {e}")
