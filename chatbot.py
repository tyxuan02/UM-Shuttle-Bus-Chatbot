# Chatbot implementation (and UI)
import json
import streamlit as st
from PIL import Image
from response import generate_response

@st.cache_data
def load_intents():
    with open('intents.json') as data:
        intents = json.load(data)
    return intents

intents = load_intents()

st.title("UM Shuttle Bus Chatbot")
st.button("Reset chat", on_click=lambda: st.session_state.pop("messages", None))

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message and message["image"] is not None:
            image = message["image"]
            displayed_image = Image.open(image)
            st.image(displayed_image)

if prompt := st.chat_input("Ask me something..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    response, image = generate_response(prompt, 0.8, intents)

    with st.chat_message("assistant"):
        st.markdown(response)
        if image is not None:
            displayed_image = Image.open(image)
            st.image(displayed_image)
    st.session_state.messages.append({"role": "assistant", "content": response, "image": image})