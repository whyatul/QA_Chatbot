from dotenv import load_dotenv  # Fixed typo
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")
chat = model.start_chat(history=[])

def get_gemini_response(prompt):
    response = chat.send_message(prompt, stream=True)
    return response

st.set_page_config(
    page_title="Q&A Chatbot",
    page_icon=":robot:",
    layout="wide",
)
st.header("Q&A Chatbot")
st.subheader("Ask me anything about the document")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input = st.text_input("Enter your question here:", key="input")
submit = st.button("Ask Me")  # Added definition for 'submit'

if submit and input:
    response = get_gemini_response(input)
    
    st.session_state['chat_history'].append({"role": "question", "text": input})  # Fixed dictionary syntax
    st.subheader("Response")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append({"role": "Bot", "text": chunk.text})  # Fixed dictionary syntax
        
st.subheader("Chat History")
for entry in st.session_state['chat_history']:  # Adjusted loop to handle list of dictionaries
    st.write(f"{entry['role']}: {entry['text']}")