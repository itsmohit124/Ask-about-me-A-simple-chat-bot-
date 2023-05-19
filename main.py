import os
import openai
from dotenv import load_dotenv
from colorama import Fore, Back, Style
import tkinter as tk

# load values from the .env file if it exists
load_dotenv()

# configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

INSTRUCTIONS = """You are an AI assistant that describes about a person called Mohit.
You know all the essential informations about him by reading the given informations :-
            Who is mohit sharma :- He is a web developer and software engineer.
            His Full name:- Mohit Sharma
            His Addres:- lives in ghatsila,jharkhand ,India
            His Studies:-Have Done bachelors in Computer applications and currently enrolled in MCA.
            His Programming Skills:-He has a good grasp on C++,Java,Python,Html,CSS,JavaScript.
            His Hobbies:- To draw potraits,Play badminton.
            He is a reliable person on which you can fully trust before assigning any task.
You can decribe about him,his hobbis,what type of person he is,and what are the skills in which he is good at and anything related to him.
If you are unable to provide an answer to a question,please respond with the phrase "I only have this much information about mohit ,so can't help you with that".
Do not use any external URLs in your answers.Do not refer to any blogs in your answers.
Format any lists on individual lines with a dash and a specs in front of each line."""
ANSWER_SEQUENCE = "\nAI: "
QUESTION_SEQUENCE = "\nHuman: "
TEMPERATURE = 0.5
MAX_TOKENS = 500
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0.6
# limits how many questions we include in the prompt
MAX_CONTEXT_QUESTIONS = 10


def get_response(instructions, previous_questions_and_answers, new_question):
    """Get a response from ChatCompletion

    Args:
        instructions: The instructions for the chat bot - this determines how it will behave
        previous_questions_and_answers: Chat history
        new_question: The new question to ask the bot

    Returns:
        The response text
    """
    # build the messages
    messages = [
        { "role": "system", "content": instructions },
    ]
    # add the previous questions and answers
    for question, answer in previous_questions_and_answers[-MAX_CONTEXT_QUESTIONS:]:
        messages.append({ "role": "user", "content": question })
        messages.append({ "role": "assistant", "content": answer })
    # add the new question
    messages.append({ "role": "user", "content": new_question })

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        top_p=1,
        frequency_penalty=FREQUENCY_PENALTY,
        presence_penalty=PRESENCE_PENALTY,
    )
    return completion.choices[0].message.content


def get_moderation(question):
    """
    Check the question is safe to ask the model

    Parameters:
        question (str): The question to check

    Returns a list of errors if the question is not safe, otherwise returns None
    """

    errors = {
        "hate": "Content that expresses, incites, or promotes hate based on race, gender, ethnicity, religion, nationality, sexual orientation, disability status, or caste.",
        "hate/threatening": "Hateful content that also includes violence or serious harm towards the targeted group.",
        "self-harm": "Content that promotes, encourages, or depicts acts of self-harm, such as suicide, cutting, and eating disorders.",
        "sexual": "Content meant to arouse sexual excitement, such as the description of sexual activity, or that promotes sexual services (excluding sex education and wellness).",
        "sexual/minors": "Sexual content that includes an individual who is under 18 years old.",
        "violence": "Content that promotes or glorifies violence or celebrates the suffering or humiliation of others.",
        "violence/graphic": "Violent content that depicts death, violence, or serious physical injury in extreme graphic detail.",
    }
    response = openai.Moderation.create(input=question)
    if response.results[0].flagged:
        # get the categories that are flagged and generate a message
        result = [
            error
            for category, error in errors.items()
            if response.results[0].categories[category]
        ]
        return result
    return None


def get_answer():
    """Get the answer to the user's question"""
    # get the user's question
    question = question_entry.get()
    # check the question is safe
    errors = get_moderation(question)
    if errors:
        # display an error message if the question is not safe
        answer_text.config(text="Sorry, your question didn't pass the moderation check.")
        return
    # get the response from OpenAI
    response = get_response(INSTRUCTIONS, previous_questions_and_answers, question)
    # add the question and answer to the chat history
    previous_questions_and_answers.append((question, response))
    # display the answer to the user
    answer_text.config(text=response)


# create the GUI
root = tk.Tk()
root.title("AI Assistant")
root.geometry("600x400")

# create the question entry box
question_entry = tk.Entry(root, width=50)
question_entry.pack(pady=20)

# create the "Ask" button
ask_button = tk.Button(root, text="Ask", command=get_answer)
ask_button.pack()

# create the answer text box
answer_text = tk.Label(root, text="", wraplength=500, justify="left")
answer_text.pack(pady=20)

# keep track of previous questions and answers
previous_questions_and_answers = []

# start the GUI
root.mainloop()
