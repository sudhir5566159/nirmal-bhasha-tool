import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Debug Mode")
st.title("🛠️ System Diagnostic")

# 1. Verify the App is New
st.success("✅ The App has successfully updated! (If you see this, the code is live)")

# 2. Test the API Key Connection
try:
    # Get key from secrets
    api_key = st.secrets["GOOGLE_API_KEY"]
    st.write(f"🔑 API Key loaded: `{api_key[:5]}...` (Hidden for safety)")
    
    # Configure Google AI
    genai.configure(api_key=api_key)
    
    # 3. ASK GOOGLE: "What models can I actually use?"
    st.subheader("📋 Models available to YOUR specific Key:")
    
    available_models = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            available_models.append(m.name)
            st.code(f"Model found: {m.name}")
            
    # 4. Try a Test Generation with the first available model
    if available_models:
        test_model = available_models[0]
        st.info(f"🧪 Testing connection with: {test_model}...")
        model = genai.GenerativeModel(test_model)
        response = model.generate_content("Hello, are you working?")
        st.success(f"🎉 SUCCESS! Response: {response.text}")
    else:
        st.error("❌ No compatible models found for this API Key. You may need to enable the API in Google Cloud Console.")

except Exception as e:
    st.error(f"⚠️ CRITICAL ERROR: {str(e)}")
