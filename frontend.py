import streamlit as st
import asyncio
from app.ai_handler import chat_with_ai

# Page Config
st.set_page_config(page_title="MCP Membership Manager", page_icon="🤖")

st.title("🤖 AI Membership Manager")
st.markdown("Ask questions like: *'How many members do we have?'* or *'List expired members'*")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask about the membership database..."):
    # 1. Show User Message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Get AI Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking & Checking Database..."):
            # We run the async function in a synchronous way for Streamlit
            response_text = asyncio.run(chat_with_ai(prompt))
            st.markdown(response_text)
            
    st.session_state.messages.append({"role": "assistant", "content": response_text})