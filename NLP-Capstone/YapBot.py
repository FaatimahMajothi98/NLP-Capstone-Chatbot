import streamlit as st
import spacy
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

st.title("YapBot")

user_input = st.text_input("You:")

if user_input:
    # Example: echo user input (replace with your chatbot logic)
    st.write("Bot: " + user_input)
