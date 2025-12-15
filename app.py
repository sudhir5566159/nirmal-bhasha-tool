import streamlit as st
from utils import show_header

# --- HOME PAGE CONFIG ---
st.set_page_config(
    page_title="ShabdaSankalan Home", 
    page_icon="🪷", 
    layout="centered"
)

# 1. TOP HEADER
show_header()

# 2. WELCOME TEXT
st.header("Welcome to the Hindi AI Suite")
st.write("Select a tool from the **Sidebar** (on the left) to begin:")
st.markdown("---")

# 3. MENU LIST (Using your Logo as the Bullet Point)

# Item 1: Nirmal Bhasha
col1, col2 = st.columns([1, 12])
with col1:
    # We use your uploaded logo, sized small (35px) to act like an icon
    st.image("nirmal_logo.png", width=35)
with col2:
    st.markdown("### **Nirmal-Bhasha**")
    st.caption("Check purity of Hindi text (Identify foreign words).")

# Item 2: Patra Lekhak
col3, col4 = st.columns([1, 12])
with col3:
    # Using the same logo for now (consistent branding)
    st.image("nirmal_logo.png", width=35)
with col4:
    st.markdown("### **Patra-Lekhak**")
    st.caption("Write formal letters instantly.")

# Item 3: Bhasha Vivek
col5, col6 = st.columns([1, 12])
with col5:
    # Using the same logo for now
    st.image("nirmal_logo.png", width=35)
with col6:
    st.markdown("### **Bhasha-Vivek**")
    st.caption("Convert Hinglish to Pure Hindi.")

# 4. FOOTER
st.markdown("---")
st.info("Developed by Sudhir K. | Powered by Gemini 2.0")
