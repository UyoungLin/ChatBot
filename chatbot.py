import random
import string
import pandas as pd
import time
import nltk
from nltk import tree, ne_chunk
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Only for the first time
# nltk.download('popular', quiet=True)
# nltk.download('punkt')
# nltk.download('wordnet')

"""
Read the corpus in csv files, which encoding is 'latin-1'
Store the questions and answers in two separate lists
"""
train_data = pd.read_csv("Dataset-2.0.csv", encoding = 'latin-1', header = None)
question_list = (train_data[1].tolist())[1:]
answer_list = train_data[2].tolist()[1:]


# Lists for keyword matching
GREETING_INPUTS = ["hi", "hello", "hey", "helloo", "hellooo", "greetings", "greeting", "sup", "what's up", "what is up"]
GREETING_REPLYS = ["Hi!", "Hi there!", "Hey!", "Hello!", "Good to see you!", "It's good seeing you!", "I am glad! You are talking to me!"]
NOTKNOW_REPLYS = ["Sorry! I have no idea.", "I'm not sure about what you mean.", "Sorry! I am still learning on this topic."]


"""Lematisation"""
def LemTokens(tokens):
    wordNetLem = WordNetLemmatizer()
    return [wordNetLem.lemmatize(token) for token in tokens]


"""Remove all the punctuations"""
def LemNormalize(text):
    punct = dict((ord(punct), None) for punct in string.punctuation)
    return LemTokens(word_tokenize(text.lower().translate(punct)))


"""Functions for simple greetings"""
def greeting(user_input):
    inputRaw = word_tokenize(user_input.lower())
    for word in inputRaw:
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_REPLYS)


"""
Game playing (hangman)
Play the game multiple times as you wish
"""
def hangman():
    print('\n')
    print('----------------------------')
    print("Welcome to Hangman!")

    words = ["vector", "standard", "control", "retrieval", "condition", "cahtbot", "coin","process","intent"]   # Word list
    word = list(words[random.randint(0, len(words) - 1)])   # Choose a random word
    guessWord = list()
    # The word to guess
    for i in range(len(word)):
        guessWord.append("_")
    wrong = 0
    win = False
    while (not win):
        print("The word: " + " ".join(guessWord))
        char = input("Guess a letter：").lower()
        if char in word:
            while char in word:
                tem_ind = word.index(char)
                guessWord[tem_ind] = char
                word[tem_ind] = '%'
            # If all the letters are correct
            if ("_" not in guessWord):
                print("Congrats! The word is " + "".join(guessWord))
                win = True
        else:
            wrong += 1
            # The user can have 5 chances
            if (wrong < 5):
                print("Wrong! Try other letters.")
                print("You still have {} chances".format(5 - wrong))
            else:
                print("You lost!")
        # The game is over, can choose to play a new one or back to the conversation
        if (wrong == 5 or win == True):
            tryAgain = input("Do you wanna try again? (y/n)").lower()
            if (tryAgain == 'y'):
                word = list(words[random.randint(0, len(words) - 1)])
                guessWord = list()
                for i in range(len(word)):
                    guessWord.append("_")
                wrong = 0
                win = False
            else:
                print('----------------------------')
                print('\n')
                print("BOT: Alright! Let have other talks!")
                break


"""
Generating reply with corpus
By comparing the cosine similarities between the user input and each questions in the list
"""
def genReply(user_input):
    reply=""
    question_list.append(user_input)    # Put the user input into the whole corpus to enrich the vocalulary
    # Return a term-document matrix, learn vocabulary and idf
    tfid_vect = TfidfVectorizer(tokenizer = LemNormalize, stop_words = None)
    train_vect = tfid_vect.fit_transform(question_list)
    # Calculate the cosine similarity between user inout and question list
    cosine_sim = cosine_similarity(train_vect[-1], train_vect)
    max_similar_ind = cosine_sim.argsort()[0][-2]   # Get the index of the question with the highest similarity to the user input
    list_sim = cosine_sim[0].tolist()   # Convert the 2D array to 1D list
    # Find the biggest cosine similarity in the list
    list_sim.sort()
    max_similar = list_sim[-2]
    # If similarity is smaller than 0.5, then the matched answer is almost meaningless, return a general answer
    if (max_similar < 0.5):
        reply = reply + random.choice(NOTKNOW_REPLYS)
        question_list.remove(user_input)    # Remove the user input from the corpus
        return reply
    # Print the matched reply
    else:
        reply = reply + answer_list[max_similar_ind]
        question_list.remove(user_input)    # Remove the user input from the corpus
        return reply          


"""
Information retrieval (user name, time, date)
"""
def infoRetrieval(user_input, username):
    inputRaw = word_tokenize(user_input)
    # Tag all the words in the sentece
    tags = pos_tag(inputRaw)

    # User's name
    if ("my name" in user_input.lower() or " am" in user_input.lower() 
        or "call me" in user_input.lower()):
        if ("do you know my name" in user_input.lower()):
            if (username == ""):
                return "Sorry, I don't know. You can tell me your name."
            else:
                return ("You are " + username)
        for ele in tags:
            # Wh-pronoun and Wh-adverb are more likely to be questions
            if (ele[1] == "WP" or ele[1] == "WRB"):
                if (username == ""):
                    return "Sorry, I don't know. You can tell me your name."
                else:
                    return ("You are " + username)

    # Current time
    elif ("time" in user_input.lower()):
        for ele in tags:
            # Wh-pronoun and modal are more likely to be questions
            if (ele[1] == "WP" or ele[1] == "MD"):
                return ("It is " + time.strftime("%H:%M", time.localtime()) + " here. ")    # Hour/Minute
    
    # Today's date
    elif ("date" in user_input.lower()):
        for ele in tags:
            # Wh-pronoun and modal are more likely to be questions
            if (ele[1] == "WP" or ele[1] == "MD"):
                return ("It is " + time.strftime("%d %b %Y", time.localtime()) + " today. ")  # Day/Month/Year
                    

"""
Remembering name and storing for later conversation
"""
def memName(user_input):
    inputRaw = word_tokenize(user_input)
    tags = pos_tag(inputRaw)    # Tag all the words in the sentece
    entities = ne_chunk(tags, binary=False)     # Use ne-chunk to determine the name entities
    userName = []
    if ("my name" in user_input.lower() or "i am" in user_input.lower() 
        or "i'm" in user_input.lower() or "call me" in user_input.lower()):
        for en in entities:
            # Find all the words that can be regarded as people's names
            if (type(en) == tree.Tree and en.label() == "PERSON"):
                for item in en:
                    userName.append(item[0])
                return userName


"""Main"""
conversation = True
name = ""
print("BOT: My name is BOT. You can:")
print("\t *Have simple conversations with me on various topics")
print("\t *Request me to remember your name (and initials should be capitalised)")
print("\t *Ask me to get some information about time or date")
print("\t *Play the Hangman game with me by typing 'hangman'")
print("If you wanna quit, just say 'bye' to me")
while (conversation == True):
    print("ME: ",end = "")
    user_input = input()
    # Quit the conversation
    if ("bye" in user_input.lower() or user_input.lower() == "goodbye"):
        conversation = False
        if (name == ""):
            print("BOT: Bye! See you.")
        else:
            print("BOT: Bye! See you " + name)
    else:
        # Enter hangman game
        if (user_input == 'hangman'):
            hangman()
        else:
            reply = "BOT: "
            # Check greeting
            if (greeting(user_input) != None):
                if (name == ""):
                    reply = reply + greeting(user_input) + " "
                else:
                    reply = reply + greeting(user_input) + " " + name + " "
            # Check infomation retrieval
            if (infoRetrieval(user_input, name) != None):
                reply = reply + infoRetrieval(user_input, name)  
            # Check remembering name   
            if (memName(user_input) != None):
                name = " ".join(memName(user_input))
                reply = reply + "Now I can remember your name is " + name + "."
            # Other replies
            if (greeting(user_input) == None and memName(user_input) == None and infoRetrieval(user_input, name) == None):
                user_input = user_input.lower()
                reply = reply + genReply(user_input)   
            print(reply)
        