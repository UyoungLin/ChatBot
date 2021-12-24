# ChatBot
### Author

Yuyang LIN



### Background

In this project, the idea for small talks was inspired by the retrieval-based chatbot from Parul Pandey (2018), which implements a TF-IDF bag of words model and calculates cosine similarity between the user input and sentences in the corpus to search for the most possible answers. As this project is merely an early-stage demo and the corpus in it is just for testing, the chatbot cannot give desirable responses to many simple questions. Thus, for the corpus part, a CSV file with both questions and answers might be suitable for a chatbot to produce meaningful answers. And here most daily questions and answers were obtained from the GitHub page of Gunther Cox, consisting of various kinds of topics to tackle with most of the daily conversations. To make the chatbot more versatile, other features like identity management and game playing were added to help the system process activities that are related to simple question answers, leading to a multi-usage NLP-based chatbot system.



### **Functionality**

In the system, there are 5 functionalities, including small daily conversations, identity memorising, information retrieval, intent matching, and game playing. And they are achieved by 5 main python functions in the code.

1. Small conversations<br>
    The daily conversation is mainly carried out by functions *greeting()* and *genReply()*. The *greeting()* function is mainly used to quickly answer some greetings and can be used in combination with the identity management function. Other general daily questions can be replied to by *genReply()*. The system will compare the user input with sentences in the corpus to give out the best-matched answers. If it cannot find a suitable answer, then the system will return a random sentence to show it is unable to respond.
2. Identity management<br>
    The function *memName()* enables the system to remember the name of the person who is currently using the system. At first, the variable storing the name is empty, and if the user mentions their name, such as saying “I am ...” or “My name is ...” or “Call me ...” then the system recognises it (including first name and last name) and remembers it until the end of the program.
3. Information retrieval<br>
    For information retrieval, *infoRetrieval()* function allows the system answer to some information queries from users. It supports three types of information, including users’ names, current times, and dates. If the user does not tell the system about their name, the system will remind the user to tell the name first, or the system will display the name of the user. Also, if the system already knows the user’s name, it will greet or say goodbye to them with their name. And for time and date, the user can simply ask “what is the time/date?” or “Could you tell me the time/date?” to get the answer.

4. Intent matching<br>
    The functionality of this section has already been mentioned in some of the previous parts, i.e., information retrieval *infoRetrieval()* and identity management *memName()*, where the user can make the system remember their name through natural language and have the system show it to them again in subsequent conversations. Also, when used to get the time or date, the system can give a clear answer.

5. Game playing<br>
    In this system, a hangman game is introduced where the user can start the game by typing “hangman”. The game is a classic word-guessing game where the user has five chances to try. When they get five wrong answers, the round fails. When the game is over, the user can choose to continue the game or exit the game to return to the conversation.
