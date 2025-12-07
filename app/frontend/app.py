import streamlit as st
import sys
import os

# 1. Fix Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.retrieval.rag_chain import build_rag_chain

st.set_page_config(page_title="RAG Observability Platform", layout="wide")
st.title("🤖 RAG Observability Platform")

if "messages" not in st.session_state:
    st.session_state.messages = []

@st.cache_resource
def load_chain():
    return build_rag_chain()

rag_chain = load_chain()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking (M4 GPU)..."):
            # LCEL Invoke (Direct String)
            response = rag_chain.invoke(prompt)
            st.markdown(response)
            
    st.session_state.messages.append({"role": "assistant", "content": response})
