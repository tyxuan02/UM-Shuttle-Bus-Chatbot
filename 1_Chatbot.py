# Chatbot implementation (and UI)
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import json
import streamlit as st
import numpy as np
from PIL import Image
from response import generate_response
from keras.models import load_model
from nlp_utils import bag_of_words, preprocess_text
import time

st.set_page_config(page_title="UM Shuttle Bus Chatbot", page_icon="🚌")

@st.cache_resource()
def load_data_and_model():
    with open('intents.json') as data:
        intents = json.load(data)

    with open('data.json') as data:
        data = json.load(data)
    
    all_words = []
    tags = []
    for intent in intents['intents']:
        tag = intent['tag']
        tags.append(tag)
        for pattern in intent['patterns']:
            words = preprocess_text(pattern)
            all_words.extend(words)

    all_words = sorted(set(all_words))
    tags = sorted(set(tags))

    model = load_model('lstm_model.h5')

    return intents, data, all_words, tags, model

def stream_response(response):
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

def get_color_confidence(confidence):
    if confidence >= 0.90:
        return "green"
    elif confidence >= 0.8:
        return "orange"
    elif confidence >= 0.75:
        return "red"

# Load data and model
intents, data, all_words, tags, model = load_data_and_model()

# Streamlit UI
st.title("🤖 UM Shuttle Bus Chatbot")
st.write("-----------\n\n")

if st.sidebar.button("Reset chat"):
    st.session_state.pop("messages", None)

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

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

    preprocessed_sentence = preprocess_text(prompt)
    X_new = np.array([bag_of_words(preprocessed_sentence, all_words)])
    y_pred = model.predict(X_new, verbose=0)
    predicted_tag = tags[np.argmax(y_pred)]
    tag_probability = y_pred[0][np.argmax(y_pred)]

    response, image = generate_response(predicted_tag, tag_probability, intents, data)

    with st.chat_message("assistant"):
        st.write_stream(stream_response(response))
    
        if image is not None:
            displayed_image = Image.open(image)
            st.image(displayed_image)

        if (tag_probability >= 0.75):
            color = get_color_confidence(tag_probability)
            st.markdown(f"<small style='color:{color}; font-weight:bold;'>Confidence Level: {tag_probability*100:.2f}%</small>", unsafe_allow_html=True)   

    st.session_state.messages.append({"role": "assistant", "content": response, "image": image})