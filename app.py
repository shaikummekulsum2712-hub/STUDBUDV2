import streamlit as st
from qa import process_and_index_file, generalize_results
from my_rag_lib.retrieval import Retriever

st.set_page_config(page_title="Study Buddy V2", layout="wide")

st.title("Study Buddy V2")
st.markdown(
    "Welcome to Study Buddy V2! Upload a file to start asking questions about your study materials."
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "retriever" not in st.session_state:
    st.session_state.retriever = None
if "current_file" not in st.session_state:
    st.session_state.current_file = None


uploaded_file = st.file_uploader(
    "Upload your file", 
    type=["pdf", "docx", "txt", "jpg", "png", "jpeg", "md", "csv"]
)

if uploaded_file is not None:
    # Process file only if it's new
    if st.session_state.current_file != uploaded_file.name:
        with st.spinner("Processing document and building FAISS index..."):
            file_bytes = uploaded_file.getvalue()
            file_name = uploaded_file.name

            # Run backend processing
            st.session_state.retriever = process_and_index_file(file_bytes, file_name)
            st.session_state.current_file = file_name
            st.session_state.chat_history = []  # Clear history for new document

        st.success(f"'{file_name}' indexed successfully!")
else:
    st.info("Please upload a file to proceed.")
    st.stop()


for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

query = st.chat_input("Ask your query here...")

if query:
    # Render user query
    st.chat_message("user").markdown(query)
    st.session_state.chat_history.append({"role": "user", "content": query})
    # 1. Cast the type so your IDE knows what methods exist
    retriever = st.session_state.get("retriever")

    # 2. Check that it is not None before calling methods
    if retriever is not None:
        # Perform retrieval
        with st.chat_message("assistant"):
            with st.spinner("Searching document..."):
                results = retriever.similarity_search(query, k=3)

                response_text = generalize_results(results)


                st.markdown(response_text)
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": response_text}
                )