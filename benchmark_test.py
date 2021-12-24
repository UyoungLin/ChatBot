import chatbot

question_set = ["How are you doing?", "Are you a dog?", "Do you play basketball?", "How old are you?", "Which book is your favourite?",
                "What is your dream?", "Are you happy with me?", "Which season do you like?", "I want to cry.", "Are you ok?",
                "Where are you now?", "Which movie do you like best?", "I want to die.", "Such a nice day.", "I feel really sad.",
                "I am afraid.", "Do you have bugs?", "You are stupid.", "What can you do?", "What is your programming language?"]
answer_set = ["I am doing well, how about you?", "No, I'm not", "I don't know how to play", "Quite young, but a million times smarter than you.", "I can't read.",
                "I dream that I will become rich.", "Happiness is not really a predictable emotion.", "Not sure.", "Sorry, I'm not sure about what you mean.", "I'm good",
                "I am on the Internet.", "Alice in Wonderland", "Maybe you should create your own chat robot to save your personality.", "I try to be as nice as I can.", "Sadness is not an emotion that I like to experience.",
                "Why?", "I am a computer programme.", "No, lots of people improve my brain.", "I can move through a network easily.  Assuming that I'm given the ability to, that is...", "I am written in Python."]

correct = 0

for i in range(20):
    ans = chatbot.genReply(question_set[i])
    if (ans == answer_set[i]):
        correct += 1
    else:
        print(question_set[i] + "// The answer is: " + ans)
    
print("----------------------------------------------------")
print("The accuracy is " + str(correct / 20))
