import streamlit as st

st.set_page_config(page_title="UM Shuttle Bus Chatbot", page_icon="🚌")

# Title
st.title("📝 Disclaimer")
st.write("-----------\n\n")

with st.container():
    st.markdown("""
    <style>
    .container {
        padding: 2rem;
        background-color: #f9f9f9;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .content {
        font-size: 1.25rem;
        color: #555;
    }
    .highlight {
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="container">
        <p class="content">
            The <span class="highlight">UM Shuttle Bus Chatbot</span> is designed to provide users with information about the UM Shuttle Bus service.
        </p>
        <p class="content">
            While we strive to provide accurate and up-to-date information, there may be instances where the chatbot provides responses that are inaccurate or differ from the actual circumstances.
        </p>
        <p class="content">
            This is due to the fact that the chatbot is trained on a limited dataset and may not have complete information about all possible scenarios.
        </p>
        <p class="content">
            We appreciate your understanding.
        </p>
    </div>
    """, unsafe_allow_html=True)