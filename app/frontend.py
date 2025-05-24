import streamlit as st
import requests
import os

st.title("Document Summarizer")

tab1, tab2 = st.tabs(["Text Input", "File Upload"])

with tab1:
    text_input = st.text_area("Enter text to summarize:", height=200)
    max_length = st.slider("Max summary length:", 50, 500, 150)
    if st.button("Summarize Text"):
        if text_input:
            response = requests.post(
                "http://localhost:8000/summarize",
                json={"text": text_input, "max_length": max_length}
            )
            if response.status_code == 200:
                st.success("Summary generated!")
                st.write(response.json()["summary"])
            else:
                st.error(f"Error: {response.json()['detail']}")

with tab2:
    uploaded_file = st.file_uploader("Upload a file (PDF, DOCX, TXT):", type=["pdf", "docx", "txt"])
    if st.button("Summarize File"):
        if uploaded_file:
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            response = requests.post("http://localhost:8000/summarize_file", files=files)
            if response.status_code == 200:
                st.success("Summary generated!")
                st.write(response.json()["summary"])
            else:
                st.error(f"Error: {response.json()['detail']}")

st.subheader("Previous Summaries")
response = requests.get("http://localhost:8000/summaries")
if response.status_code == 200:
    summaries = response.json()["summaries"]
    for summary in summaries:
        st.write(f"ID: {summary['id']}, Input: {summary['input_text'][:100]}..., Summary: {summary['summary']}")
else:
    st.error("Failed to fetch summaries")