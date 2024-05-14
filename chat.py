# Chatbot implementation (and UI)
import json
import streamlit as st
from response import generate_response

@st.cache_data
def load_intents():
    with open('intents.json') as data:
        intents = json.load(data)
    return intents

intents = load_intents()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me something..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    response, image = generate_response(prompt, 0.8, intents)
    # if image is not None:
    #     response = response + "image"

    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})