import streamlit as st
import requests

st.title("🎙️ Podcast Summarizer App")

# File uploader
uploaded_file = st.file_uploader("Upload your audio file", type=["mp3", "wav", "m4a"])

if uploaded_file is not None:
    # Show filename
    st.write(f"Uploaded: {uploaded_file.name}")

    # Backend ka URL
    BACKEND_URL = "http://127.0.0.1:8000/summarize"

    # Upload button
    if st.button("Generate Summary"):
        files = {"file": uploaded_file.getvalue()}
        response = requests.post(BACKEND_URL, files={"file": uploaded_file})
        
        if response.status_code == 200:
            summary = response.json().get("summary", "⚠️ No summary returned")
            st.subheader("📄 Summary")
            st.write(summary)
        else:
            st.error("❌ Error: Backend se summary nahi mili.")
