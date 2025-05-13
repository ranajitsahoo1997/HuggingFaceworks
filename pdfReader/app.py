# app.py
import streamlit as st
from pdf_utils import load_and_split_pdf, store_in_faiss, extract_topics, generate_mcqs
import tempfile

st.set_page_config(page_title="PDF Topic Quiz Generator", layout="wide")
st.title("📘 PDF Topic-Based MCQ Generator")

# Upload PDF
uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    st.success("PDF uploaded successfully!")

    with st.spinner("Reading and processing the PDF..."):
        docs = load_and_split_pdf(tmp_path)
        st.write(f"Extracted {len(docs)} pages from the PDF.")
        st.write("Storing in FAISS...")
        vectorstore = store_in_faiss(docs)
        st.success("Stored in FAISS successfully!")
        st.write("Extracting topics...")
        topics_list = extract_topics(docs)
        st.success("Topics extracted successfully!")
        st.write("You can now generate MCQs based on the topics listed below.")

    if topics_list:
        st.subheader("📚 Available Topics")
        st.write(topics_list)

        selected_topic = st.text_input("Enter a topic to generate MCQs:")
        if selected_topic:
            with st.spinner("Generating MCQs..."):
                mcqs = generate_mcqs(vectorstore, selected_topic)
                st.subheader("📝 MCQs")
                st.markdown(mcqs)
else:
    st.info("Please upload a PDF file to begin.")