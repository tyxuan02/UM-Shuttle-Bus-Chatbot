import streamlit as st

st.set_page_config(page_title="UM Shuttle Bus Chatbot", page_icon="🚌")

# Title
st.title("📝 UM Shuttle Bus Chatbot Guide")

st.write("-----------\n\n")

# Introduction
st.markdown("""
Welcome to the UM Shuttle Bus Chatbot! This chatbot is designed to provide information about the UM Shuttle Bus service. Here are some examples of the types of questions you can ask:
""")

# Sections with questions
st.subheader("Bus Routes")
st.markdown("""
- What are the bus routes?
- Can you show me the route for each bus?
- Where are the shuttle bus stops for route AB?
""")

st.subheader("Bus Schedule")
st.markdown("""
- When is the next trip for route 13?
- What is the bus schedule for today?
- Can you show me the schedule for bus E?
""")

st.subheader("Bus Frequency")
st.markdown("""
- How often do the buses run?
- When do the shuttle buses start running?
- How long does the shuttle bus take to travel from one stop to another?
""")

st.subheader("General Information")
st.markdown("""
- What are the operating hours for the bus service?
- Do I need to have a UM student card to take the shuttle bus?
- Who should I contact if I left something on a shuttle bus?
- Are there any specific guidelines for using the shuttle bus service?
- Can I reserve the shuttle bus for a special event?
""")

# Reminder
st.write("\n\n")
st.markdown("""
**Remember**, the chatbot is trained on a limited dataset, so there may be some questions it can't answer accurately. If you have a question that the chatbot can't answer, or if you need more detailed information, we recommend checking the official UM Shuttle Bus service resources.
""")