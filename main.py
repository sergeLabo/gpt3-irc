

import os
from dotenv import load_dotenv
import openai


load_dotenv()
openai.api_key = os.environ.get('OPENAI_KEY')
completion = openai.Completion()

start_chat_log = '''Human: Bonjour, comment va-tu?
AI: Salut, je suis un robot intelligent.
Human:Quelle heure est-il?
AI:Il est 19h09
Human:Qui est Joseph?
AI:C'est un dragon.
'''


def ask(question, chat_log=None):
    """
    prompt: the input text
    engine: OpenAI has made four text completion engines available, named 
            davinci, ada, babbage and curie.
            We are using davinci, which is the most capable of thefour.
    stop:   As I mentioned earlier, the GPT-3 engine does not really understand text, 
            so when it completes text it needs to know when to stop. 
            By giving a stop of Human: we are telling the engine to just generate 
            text for the line that begins with AI:. Without a stop marker 
            GPT-3 would continue generating text by writing more lines 
            for both the user and the AI.
    temperature:    a number between 0 and 1 that determines how many creative 
                    risks the engine takes when generating text.
    top_p:  an alternative way to control the originality and creativity of 
            the generated text.
    frequency_penalty:  a number between 0 and 1. The higher this value the model 
                        will make a bigger effort in not repeating itself.
    presence_penalty:   a number between 0 and 1. The higher this value the model 
                        will make a bigger effort in talking about new topics.
    max_tokens: maximum completion length.
    """
    if chat_log is None:
        chat_log = start_chat_log
    prompt = f'{chat_log}Human: {question}\nAI:'
    response = completion.create(
        prompt=prompt, engine="davinci", stop=['\nHuman'], temperature=0.9,
        top_p=1, frequency_penalty=0, presence_penalty=0.6, best_of=1,
        max_tokens=150)
    answer = response.choices[0].text.strip()
    return answer


def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None:
        chat_log = start_chat_log
    return f'{chat_log}Human: {question}\nAI: {answer}\n'


chat_log = None

question = 'Qui joue Forrest Gump dans le film?'
answer = ask(question, chat_log)
print('\n\nQuestion', question)
print('Robot:', answer)

chat_log = append_interaction_to_chat_log(question, answer, chat_log)

question = 'Dans quel autre film célèbre a-t-il joué?'
answer = ask(question, chat_log)
print('\n\nQuestion', question)
print('Robot:', answer)

chat_log = append_interaction_to_chat_log(question, answer, chat_log)

question = 'Qui est le président de la France?'
answer = ask(question, chat_log)
print('\n\nQuestion', question)
print('Robot:', answer)

chat_log = append_interaction_to_chat_log(question, answer, chat_log)
question = 'Connais-tu La Labomedia?'
answer = ask(question, chat_log)
print('\n\nQuestion', question)
print('Robot:', answer)

