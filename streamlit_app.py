import streamlit as st
from services.chat_service import ChatService

st.title("LangChain Chatbot")
st.header("Conversational Model with memory", divider="red")

if "service" not in st.session_state:
    st.session_state.service = ChatService(thread_id="streamlit-session")

if "messages" not in st.session_state:
    history = st.session_state.service.get_history()
    st.session_state.messages = [
        msg for msg in history
        if msg.type in ["human", "ai"]
    ]

for message in st.session_state.messages:
    with st.chat_message(message.type):
        st.write(message.content)

if prompt := st.chat_input("Escribe tu mensaje"):

    st.session_state.messages.append(
        {"type": "human", "content": prompt}
    )
    with st.chat_message("human"):
        st.write(prompt)

    response = st.session_state.service.send_message(prompt)

    st.session_state.messages.append(
        {"type": "ai", "content": response}
    )
    with st.chat_message("ai"):
        st.write(response)
