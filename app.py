import streamlit as st
from utils import show_header, get_daily_word, save_subscriber

# --- PAGE CONFIG ---
st.set_page_config(page_title="ShabdaSankalan Home", page_icon="🪷", layout="centered")

# --- SIDEBAR POWER STATION ---
with st.sidebar:
    # 1. DAILY HOOK
    st.markdown("### 🌟 Aaj Ka Shabd (Today's Word)")
    daily = get_daily_word()
    st.info(f"**{daily['word']}**\n\n{daily['meaning']}")
    
    st.markdown("---")
    
    # 2. LEAD MAGNET (Hormozi Style)
    st.markdown("### 🎁 Free Gift")
    st.caption("Get the **'100 Most Powerful Hindi Words'** PDF directly in your inbox.")
    email = st.text_input("Enter Email:", placeholder="name@example.com")
    if st.button("Send me the PDF 📥"):
        if email and "@" in email:
            save_subscriber(email)
            st.success("Success! Check your inbox soon.")
        else:
            st.error("Please enter a valid email.")
            
    st.markdown("---")
    
    # 3. MONETIZATION
    st.markdown("### ☕ Support Us")
    st.caption("We keep this tool free for students. If it helped you, fuel us with a chai!")
    st.markdown("[![Support via UPI](https://img.shields.io/badge/Support-UPI%2FDonate-orange?style=for-the-badge&logo=bhim)](https://www.google.com)")

# --- MAIN PAGE CONTENT ---
show_header()

st.header("Welcome to the Hindi AI Suite")
st.write("Select a tool from the **Sidebar** to begin your journey to pure Hindi.")
st.markdown("---")

# Item 1: Nirmal Bhasha
col1, col2 = st.columns([1, 12])
with col1:
    try: st.image("nirmal_logo.png", width=40)
    except: st.write("🪷")
with col2:
    st.markdown("### **Nirmal-Bhasha**")
    st.caption("Check purity of Hindi text (Identify foreign words).")

# Item 2: Patra Lekhak
col3, col4 = st.columns([1, 12])
with col3:
    st.markdown("<h2 style='text-align: center; margin: 0; color: #ff4b4b;'>02</h2>", unsafe_allow_html=True)
with col4:
    st.markdown("### **Patra-Lekhak**")
    st.caption("Write formal letters instantly.")

# Item 3: Bhasha Vivek
col5, col6 = st.columns([1, 12])
with col5:
    st.markdown("<h2 style='text-align: center; margin: 0; color: #ff4b4b;'>03</h2>", unsafe_allow_html=True)
with col6:
    st.markdown("### **Bhasha-Vivek**")
    st.caption("Convert Hinglish to Pure Hindi.")
    
# Item 4: Nibandh Lekhak
col7, col8 = st.columns([1, 12])
with col7:
    st.markdown("<h2 style='text-align: center; margin: 0; color: #ff4b4b;'>04</h2>", unsafe_allow_html=True)
with col8:
    st.markdown("### **Nibandh-Lekhan**")
    st.caption("Generate structured essays for Exams/UPSC.")

st.markdown("---")
st.info("Developed by Shabdasankalan Team | Powered by Gemini 2.5")
