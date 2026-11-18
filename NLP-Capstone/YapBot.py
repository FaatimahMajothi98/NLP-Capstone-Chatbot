# Import setup libraries
import streamlit as st
import string
import spacy

#--------------------------------------------------------

# Load spaCy model
word2vec = spacy.load('en_core_web_sm')

# Exit commands
exit_commands = ("quit", "goodbye", "exit", "no", "nothing", "never mind", "bye", "end", "stop")

#--------------------------------------------------------

# Clean text function
def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return " ".join(text.split())

#--------------------------------------------------------

# Load and preprocess conversation data
with open('train-data/human_chat.txt', 'r') as file:
    lines = file.readlines()

conversations = []
current_convo = []

for line in lines:
    if line.lower().startswith("human 1: hi"):
        if current_convo:
            conversations.append(current_convo)
            current_convo = []
    current_convo.append(line.strip())
if current_convo:
    conversations.append(current_convo)

questions = []
answers = []

for convo in conversations:
    for i in range(len(convo)-1):
        if convo[i].startswith("Human 1:") and convo[i+1].startswith("Human 2:"):
            q = convo[i].split(":", 1)[1].strip()
            a = convo[i+1].split(":", 1)[1].strip()
            questions.append(q)
            answers.append(a)

#--------------------------------------------------------

# YapBot class
class YapBot:
    def __init__(self, questions, answers, name="User"):
        self.questions = [clean_text(q) for q in questions]
        self.answers = answers
        self.name = name

    def compare_similarity(self, user_message, possible_response):
        user_doc = word2vec(user_message)
        response_doc = word2vec(possible_response)
        return user_doc.similarity(response_doc)

    def respond(self, user_message):
        cleaned_input = clean_text(user_message)
        similarity_scores = [self.compare_similarity(cleaned_input, q) for q in self.questions]
        if max(similarity_scores) < 0.7:
            return f"Sorry, {self.name}, I didn't understand that. Can you try again?"
        best_match_index = similarity_scores.index(max(similarity_scores))
        return self.answers[best_match_index]
    
#--------------------------------------------------------

# Initialise YapBot

bot = YapBot(questions, answers)

# Connect to Streamlit

st.title("YapBot")

if 'history' not in st.session_state:

    st.session_state['history'] = []

if 'initialized' not in st.session_state:

    st.session_state['history'].append(("YapBot", "Hello there! I'm YapBot. Ask me anything!"))
    st.session_state['initialized'] = True

user_input = st.text_input("Your questions here:", key="input")

if st.button("Send"):

    if user_input:

        response = bot.respond(user_input)
        st.session_state['history'].append(("You", user_input))
        st.session_state['history'].append(("YapBot", response))

for speaker, message in st.session_state['history']:

    st.write(f"**{speaker}:** {message}")
