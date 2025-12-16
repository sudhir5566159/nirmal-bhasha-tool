import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Admin", page_icon="🔐", layout="centered")
password = st.text_input("Admin Password:", type="password")

if password == "Sudhir123":
    st.success("Access Granted")
    
    # FEEDBACK TAB
    tab1, tab2 = st.tabs(["Feedback Logs", "Subscribers"])
    
    with tab1:
        if os.path.exists("feedback_log.csv"):
            df = pd.read_csv("feedback_log.csv")
            st.dataframe(df)
            with open("feedback_log.csv", "rb") as f:
                st.download_button("📥 Download Feedback CSV", f, "feedback.csv")
        else: st.warning("No feedback yet.")

    with tab2:
        if os.path.exists("subscribers.csv"):
            df_sub = pd.read_csv("subscribers.csv")
            st.dataframe(df_sub)
            with open("subscribers.csv", "rb") as f:
                st.download_button("📥 Download Subscribers CSV", f, "subscribers.csv")
        else: st.warning("No subscribers yet.")
