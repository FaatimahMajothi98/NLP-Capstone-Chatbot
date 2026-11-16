# Import libraries

# {pip install streamlit spacy nltk} if needed
import re
from collections import Counter
import spacy
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

word2vec = spacy.load('en_core_web_sm')
stop_words = set(stopwords.words("english"))

# Import and prepare data
with open('human_text.txt', 'r') as file:
    lines = file.readlines()

questions = []
answers = []

for line in lines:
    parts = line.split(':', 1)
    if len(parts) == 2:
        label = parts[0].strip()
        message = parts[1].strip()
        if label == "Human 1":
            questions.append(message)
        elif label == "Human 2":
            answers.append(message)



# Create list of exit commands
exit_commands = ("quit", "goodbye", "exit", "no", "nothing", "never mind", "bye", "end", "stop")

# Create  initial functions
def preprocess(input_sentence):
    input_sentence = input_sentence.lower()
    input_sentence = re.sub(r'[^\w\s]','',input_sentence)
    tokens = word_tokenize(input_sentence)
    input_sentence = [i for i in tokens if not i in stop_words]
    return(input_sentence)

def compare_overlap(user_message, possible_response):
    similar_words = 0
    for token in user_message:
        if token in possible_response:
              similar_words += 1
    return similar_words
  

def compute_similarity(tokens, category):
    output_list = list()
    for token in tokens:
        output_list.append([token.text, category.text, token.similarity(category)])
    return output_list



class ChatBot:
  
  # Define exit function:
  def make_exit(self, user_message):
    for command in exit_commands:
      if command in user_message:
        print("Goodbye!")
        return True
      
  # Define chat function:
  def chat(self):
    print("Initiating chat... to exit at any point, enter an exit word.")
    print("loading...")
    for i in range(0,3):
       print(f"{i}...")
    user_message = input("Hello human! ")
    self.name = input("What may I call you? ")
    #while not self.make_exit(user_message):
    #  user_message = self.respond(user_message)










bot = ChatBot()
ChatBot.chat()