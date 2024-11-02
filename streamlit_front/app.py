import streamlit as st 
from pags.main_page import chatbot_page

st.set_page_config(page_title="Intents chatbot", page_icon="🚀", layout="wide")

chatbot_page()