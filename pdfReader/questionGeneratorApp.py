import streamlit as st
import tempfile
from questionGeneratorUtils import pdf_reader, generate_questions

st.set_page_config(page_title="Quiz Generator", layout="wide", page_icon="📘")



st.title("RedIntegro AI Based Quiz Generator")

st.write("This is a demo application that generates quiz questions from a PDF file using AI. The application uses the Langchain library to process the PDF and generate questions. The application is built using Streamlit, a Python library for building web applications.")
st.write("To use the application, please upload a PDF file. The application will then process the file and generate quiz questions based on the content of the PDF. The questions will be displayed on the screen along with their answers.")
st.write("The application uses the Ollama model to generate questions. The model is a large language model that has been trained on a wide range of topics. The model is able to generate questions that are relevant to the content of the PDF file.")
st.write("Once the questions are generated, you can review them and use them as needed.")
st.write("Please upload a PDF file to get started.")
tmp_path = ""
uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])
data = None
if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name
    st.success("PDF uploaded successfully!")


    
    with st.spinner("Loading and Processing the PDF..."):
        documents, llm = pdf_reader(tmp_path)
        st.success("PDF loaded and processed successfully!")
        st.write(f"Extracted {len(documents)} pages from the PDF.")
        st.write("Generating questions...")
        question_gen_response = generate_questions(documents,llm)
        st.success("Questions generated successfully!")
        # print(question_gen_response)
        # st.write(question_gen_response)

        st.title("🧠 Java Quiz App")
        data = question_gen_response
if data is not None:
    # Step 1: Select category
    categories = list(data.keys())
    category = st.selectbox("Select a quiz category", categories)

    # Step 2: Load questions for that category
    questions = data[category]

    # Session state management
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
    if "selected_option" not in st.session_state:
        st.session_state.selected_option = None
    if "show_answer" not in st.session_state:
        st.session_state.show_answer = False

    st.markdown("### Questions")

    # Step 3: Show buttons for each question
    for i, q in enumerate(questions):
        if q["question"]:
            if st.button(f"Question {i+1}: {q['question'][:40]}..."):
                st.session_state.current_question = i
                st.session_state.selected_option = None
                st.session_state.show_answer = False

    # Step 4: Display selected question and options
    if st.session_state.current_question is not None:
        q_index = st.session_state.current_question
        q_data = questions[q_index]

        st.subheader(q_data["question"])
        for option in q_data["options"]:
            if st.button(option, key=f"{q_index}_{option}"):
                st.session_state.selected_option = option
                st.session_state.show_answer = True

        # Step 5: Show answer
        if st.session_state.show_answer and st.session_state.selected_option:
            st.success(q_data["answer"])