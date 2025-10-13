import streamlit as st
from PyPDF2 import PdfReader
import requests

st.title("📄 Free AI Summarizer (Text or PDF)")

# Hugging Face API token
HF_TOKEN = "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"
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

def summarize_text(text):
    response = requests.post(API_URL, headers=HEADERS, json={"inputs": text})
    if response.status_code == 200:
        return response.json()[0]["summary_text"]
    else:
        return f"Error: {response.status_code}"

# Option to choose input
option = st.radio("Select input method:", ("Upload PDF", "Type / Paste Text"))

text_to_summarize = ""

if option == "Upload PDF":
    uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])
    if uploaded_file is not None:
        reader = PdfReader(uploaded_file)
        text_to_summarize = ""
        for page in reader.pages:
            text_to_summarize += page.extract_text()
        st.subheader("Preview (first 1000 characters):")
        st.write(text_to_summarize[:1000] + "..." if len(text_to_summarize) > 1000 else text_to_summarize)

elif option == "Type / Paste Text":
    text_to_summarize = st.text_area("Enter your text here:", height=200)

# Summarize button for both input methods
if st.button("Summarize", key="summarize_button"):
    if text_to_summarize.strip() != "":
        st.subheader("Summarizing...")
        summary = summarize_text(text_to_summarize[:4000])
        st.subheader("🧠 AI Summary")
        st.write(summary)
    else:
        st.warning("Please provide text or upload a PDF first!")
