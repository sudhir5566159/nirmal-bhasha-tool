import streamlit as st
from utils import show_header

# --- FIX: Updated Icon to Lotus ---
st.set_page_config(
    page_title="ShabdaSankalan Home", 
    page_icon="🪷", 
    layout="centered"
)

show_header() # Shows the Pink SVG Lotus

st.header("Welcome to the Hindi AI Suite")
st.write("""
Select a tool from the **Sidebar** (on the left) to begin:

- **🪷 Nirmal-Bhasha:** Check purity of Hindi text.
- **📝 Patra-Lekhak:** Write formal letters instantly.
- **🧪 Bhasha-Vivek:** Convert Hinglish to Pure Hindi.
""")

st.info("Developed by Sudhir K. | Powered by Gemini 2.0")
