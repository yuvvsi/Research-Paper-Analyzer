import streamlit as st
from paper_parser import extract_text_from_pdf, extract_text_from_docx
from chat_engine import chat_with_llm

st.set_page_config(page_title="📄 Paper Weakness Detector + Chat", layout="wide")
st.title("🧠 Research Paper Analyzer (Chat + One-Click Review)")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# File uploader
uploaded_file = st.file_uploader("Upload a research paper (PDF or DOCX)", type=["pdf", "docx"])

# Process uploaded file
if uploaded_file and "paper_text" not in st.session_state:
    file_type = uploaded_file.type
    if file_type == "application/pdf":
        paper_text = extract_text_from_pdf(uploaded_file)
    elif file_type in [
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/docx"
    ]:
        paper_text = extract_text_from_docx(uploaded_file)
    else:
        st.error("Unsupported file type.")
        paper_text = ""

    st.session_state.paper_text = paper_text
    st.session_state.chat_history.append({
        "role": "system",
        "content": "You are an academic writing expert. Analyze and answer questions based on this paper:\n" + paper_text[:5000]
    })

# If paper is uploaded
if "paper_text" in st.session_state:
    st.subheader("📄 Extracted Paper Text")
    with st.expander("Click to view", expanded=False):
        st.text_area("Text", st.session_state.paper_text, height=300)

    if st.button("🔍 Analyze Methodological Weaknesses"):
        with st.spinner("Talking to the LLM..."):
            prompt = f"Please analyze the following research paper and identify any methodological weaknesses, clarity issues, or missing components:\n\n{st.session_state.paper_text}"
            feedback = chat_with_llm(prompt)
            st.session_state.last_feedback = feedback

    if "last_feedback" in st.session_state:
        st.subheader("📌 One-Click LLM Feedback")
        st.markdown(st.session_state.last_feedback)

    st.subheader("💬 Chat with the LLM about this paper")
    user_input = st.chat_input("Ask about methodology, improvements, or any doubts...")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        with st.spinner("LLM is typing..."):
            reply = chat_with_llm(messages=st.session_state.chat_history)
            st.session_state.chat_history.append({"role": "assistant", "content": reply})

    for msg in st.session_state.chat_history[1:]:
        if msg["role"] == "user":
            st.chat_message("user").markdown(msg["content"])
        elif msg["role"] == "assistant":
            st.chat_message("assistant").markdown(msg["content"])