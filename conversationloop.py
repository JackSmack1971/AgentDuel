import openai
import os
import json
import logging
from collections import deque
from dotenv import load_dotenv
from typing import Deque
from tkinter import Tk, Label, Button, Entry, StringVar, OptionMenu 

# Load environment variables from .env file
load_dotenv() 

# Set up logging
logging.basicConfig(level=logging.INFO) 

# Load the OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY', 'default_value') 

# Check if OpenAI API key is set
if openai.api_key == 'default_value':
    logging.error("OPENAI_API_KEY is not set in the environment variables.")
    exit(1) 

# Define the chat models
chat_model = "gpt-3.5-turbo" 

# Define the system roles
chatbot1_role = ''
chatbot2_role = '' 

# Function to read system roles from text files
def read_file(file_name: str) -> str:
    """Reads a file and returns its content. Handles errors for file not found, permission error, and directory error."""
    global chatbot1_role
    global chatbot2_role
    try:
        with open(file_name, 'r') as file:
            if file_name == 'Mrs_Writer.txt':
                chatbot1_role = file.read().replace('\n', '')
            elif file_name == 'Mr_Editor.txt':
                chatbot2_role = file.read().replace('\n', '')
    except (FileNotFoundError, PermissionError, IsADirectoryError, IOError) as e:
        logging.error(f"Error reading {file_name}: {e}") 

read_file('Mrs_Writer.txt')
read_file('Mr_Editor.txt') 

def initialize_conversation() -> Deque:
    """Initializes the conversation with system roles."""
    conversation = deque()
    conversation.append({"role": "system", "content": f"I'm a helpful assistant. {chatbot1_role}"})
    conversation.append({"role": "system", "content": f"I'm a helpful assistant. {chatbot2_role}"})
    return conversation 

def conversation_loop(conversation: Deque, content_type: str, subject_matter: str) -> None:
    """Defines the conversation loop between the two chatbots."""
    try:
        for i in range(10):
            for chatbot_role in [(chatbot1_role, "Mrs Writer"), (chatbot2_role, "Mr Editor")]:
                message = {"role": "user", "content": f"{chatbot_role[1]}'s turn. {chatbot_role[0]}"}
                conversation.append(message)
                response = openai.ChatCompletion.create(model=chat_model, messages=list(conversation), timeout=10)
                conversation.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
    except Exception as e:
        logging.error(f"An error occurred: {e}") 

def print_conversation(conversation: Deque) -> None:
    """Prints the conversation."""
    for message in conversation:
        print(f"{message['role']}: {message['content']}") 

class UserInput:
    """Class for GUI user input.""" 

    def __init__(self, master):
        self.master = master
        master.title("Content Creation") 

        self.content_type = StringVar(master)
        self.content_type.set("Article")  # default value 

        self.label = Label(master, text="Content Type:")
        self.option = OptionMenu(master, self.content_type, "Article", "Blog Post", "Short Story")
                self.label2 = Label(master, text="Subject Matter:")
        self.entry = Entry(master) 

        self.submit_button = Button(master, text="Submit", command=self.submit) 

        self.label.pack()
        self.option.pack()
        self.label2.pack()
        self.entry.pack()
        self.submit_button.pack() 

    def submit(self):
        """Submits the user input and starts the conversation loop."""
        content_type = self.content_type.get()
        subject_matter = self.entry.get()
        conversation = initialize_conversation()
        conversation_loop(conversation, content_type, subject_matter)
        print_conversation(conversation) 

root = Tk()
user_input = UserInput(root)
root.mainloop()
