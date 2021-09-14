"""Sending GPT-3 requests from Python

In this section we are going to create the support code that will allow us to work with the OpenAI GPT-3 engine. The code will be stored in a file called chatbot.py. Below you can see the initialization section of this file:
"""

import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.environ.get('OPENAI_KEY')
completion = openai.Completion()

start_chat_log = '''Human: Hello, who are you?
AI: I am doing great. How can I help you today?
'''

"""
The load_dotenv() function imports any variables stored in a .env file as environment variables. Note how we use the OPENAI_KEY variable in the following line to initialize OpenAI with the key. The completion variable holds the actual client to the engine. This is the object we will use to send queries.

I also added a start_chat_log variable, containing the two lines that prime the engine. Once the bot is up and running I encourage you to try different interactions in this variable to see how the bot changes its responses accordingly.

Let’s now write a function that makes a GPT-3 query. Add the following function at the bottom of chatbot.py:
"""

def ask(question, chat_log=None):
    if chat_log is None:
        chat_log = start_chat_log
    prompt = f'{chat_log}Human: {question}\nAI:'
    response = completion.create(
        prompt=prompt, engine="davinci", stop=['\nHuman'], temperature=0.9,
        top_p=1, frequency_penalty=0, presence_penalty=0.6, best_of=1,
        max_tokens=150)
    answer = response.choices[0].text.strip()
    return answer

"""
The ask() function takes the question from the user as a first argument, followed by an optional chat log. If the chat log is not provided then the function uses start_chat_log instead.

The prompt variable is built to contain the chat log, followed by the question from the user, which is prefixed with Human: . After the user question we add final line reading just AI:, which is what is going to give the GPT-3 engine the queue to generate a response to the user’s question.

The completion.create() function is where the request to the GPT-3 engine is actually made. This function takes a number of arguments, which are used to configure how the engine should complete the text. Here is a brief description of these arguments:

    prompt: the input text
    engine: OpenAI has made four text completion engines available, named davinci, ada, babbage and curie. We are using davinci, which is the most capable of the four.
    stop: As I mentioned earlier, the GPT-3 engine does not really understand text, so when it completes text it needs to know when to stop. By giving a stop of Human: we are telling the engine to just generate text for the line that begins with AI:. Without a stop marker GPT-3 would continue generating text by writing more lines for both the user and the AI.
    temperature: a number between 0 and 1 that determines how many creative risks the engine takes when generating text.
    top_p: an alternative way to control the originality and creativity of the generated text.
    frequency_penalty: a number between 0 and 1. The higher this value the model will make a bigger effort in not repeating itself.
    presence_penalty: a number between 0 and 1. The higher this value the model will make a bigger effort in talking about new topics.
    max_tokens: maximum completion length.

These are not the only possible options, so I recommend you review the OpenAI reference documentation to learn about more ways to configure your request.

The response from the completion engine is an object that has a choices attribute, which is a list of completions. We haven’t requested multiple completions, so the list is going to have a single element. This element is a Python dictionary with a text key that contains the generated text. Our function takes this text, removes any leading or trailing whitespace and returns it back to the caller. As mentioned above, consult the API documentation for information on other data items included in the GPT-3 response.

Let’s start a Python shell and play with the ask() function:

"""

>>> from chatbot import ask
>>> ask('Who played Forrest Gump in the movie?')
'Oh my, that is a tough one! Forrest Gump was played by Tom Hanks.'
>>> ask('How long does it take to travel from Los Angeles to Dublin?')
'It takes about 12 hours to fly from Los Angeles to Dublin. You may want to fly through Heathrow Airport in London.'

"""
Pretty cool, right? What we are missing is the second part of our algorithm, in which we append a question and its response to the chat log, so that we can use it in the following question. We can implement a second function to update the chat log:
"""

def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None:
        chat_log = start_chat_log
    return f'{chat_log}Human: {question}\nAI: {answer}\n'

"""
This function takes a question and an answer, and adds them at the bottom of the chat log. The updated chat log is returned.

Now we can have a conversation in which the context is preserved. Try the following in a new Python shell session:
"""

>>> from chatbot import ask, append_interaction_to_chat_log
>>> chat_log = None

>>> question = 'Who played Forrest Gump in the movie?'
>>> answer = ask(question, chat_log)
>>> answer
'Forrest Gump is a 1994 American romantic comedy-drama film based on the 1986 novel of the same name by Winston Groom. The film was directed by Robert Zemeckis and was adapted for the screen by Eric Roth. It stars Tom Hanks as Forrest Gump, for which he won the Academy Award for Best Actor, and was nominated for Best Picture.'

>>> chat_log = append_interaction_to_chat_log(question, answer, chat_log)

>>> question = 'Was he in any other great roles?'
>>> answer = ask(question, chat_log)
>>> answer
'He played the protagonist in The Green Mile (1999), a drama film based on the Stephen King novel of the same name.'

"""
These two functions are all we need to manage our chat. In the next sections we are going to integrate them with Twilio SMS messaging.
"""
