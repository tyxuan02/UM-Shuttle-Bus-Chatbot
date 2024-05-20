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

@st.cache_data
def load_intents():
    with open('intents.json') as data:
        intents = json.load(data)
    return intents

@st.cache_data
def load_words_and_tags():
    all_words = []
    tags = []
    # loop through each sentence in our intents patterns
    for intent in intents['intents']:
        tag = intent['tag']
        # add to tag list
        tags.append(tag)
        for pattern in intent['patterns']:
            # text preprocessing
            words = preprocess_text(pattern)
            # add to our words list
            all_words.extend(words)

    # remove duplicates and sort
    all_words = sorted(set(all_words))
    tags = sorted(set(tags))

    return all_words, tags

@st.cache_resource()
def load_model_once():
    print("hi")
    model = load_model('lstm_model.h5')
    return model

# Load the model
model = load_model_once()

intents = load_intents()
all_words, tags = load_words_and_tags()



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

    preprocessed_sentence = preprocess_text(prompt)
    X_new = np.array([bag_of_words(preprocessed_sentence, all_words)])
    y_pred = model.predict(X_new, verbose=0)
    predicted_tag = tags[np.argmax(y_pred)]
    tag_probability = y_pred[0][np.argmax(y_pred)]
    print(predicted_tag, tag_probability)

    response, image = generate_response(predicted_tag, tag_probability, intents)

    with st.chat_message("assistant"):
        st.markdown(response)
        if image is not None:
            displayed_image = Image.open(image)
            st.image(displayed_image)
    st.session_state.messages.append({"role": "assistant", "content": response, "image": image})