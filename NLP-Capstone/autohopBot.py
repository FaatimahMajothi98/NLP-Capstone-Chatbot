# Import libraries
import re
from collections import Counter
import spacy
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

word2vec = spacy.load('en_core_web_sm')
stop_words = set(stopwords.words("english"))




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
  
def extract_nouns(tagged_message):
    message_nouns = list()
    for token in tagged_message:
        if token[1].startswith("N"):
            message_nouns.append(token[0])
    return message_nouns

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
        print("Okay, have a nice day.")
        return True
      
  # Define chat function:
  def chat(self):
    user_message = input("Welcome to AutoHopper! What can I help you with today? ")
    while not self.make_exit(user_message):
      user_message = self.respond(user_message)