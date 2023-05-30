import openai
import os
import json
import logging
from collections import deque
from dotenv import load_dotenv
from typing import deque
from tkinter import tk, label, button, entry, stringvar, optionmenu

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load the OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the chat models
chat_model = "gpt-3.5-turbo"

# Define the system roles
chatbot1_role = ""
chatbot2_role = ""

def read_file(filename: str) -> str:
    """
    Function to read system roles from text files
    """
    global chatbot1_role
    global chatbot2_role
    try:
        with open(filename, 'r') as file:
            if filename == "Mrs_Writer.txt":
                chatbot1_role = file.read().replace('\n', '')
            elif filename == "Mr_Editor.txt":
                chatbot2_role = file.read().replace('\n', '')
    except (FileNotFoundError, PermissionError, IsADirectoryError, IOError) as e:
        logging.error(f"Error reading {filename}: {e}")

def initialize_conversation() -> deque:
    """
    Function to initialize the conversation
    """
    conversation = deque()
    conversation.append({"role": "system", "content": f"I'm a helpful assistant. {chatbot1_role}"})
    conversation.append({"role": "system", "content": f"I'm a helpful assistant. {chatbot2_role}"})
    return conversation

def conversation_loop(conversation: deque, content_type: str, subject_matter: str) -> None:
    """
    Function to run the conversation loop
    """
    try:
        for i in range(10):
            for chatbot_role in [chatbot1_role, chatbot2_role]:
                message = {"role": "user", "content": f"{chatbot_role}'s turn. {chatbot_role[0]}"}
                conversation.append(message)
                response = openai.ChatCompletion.create(
                    model=chat_model,
                    messages=list(conversation),
                    timeout=10
                )
                if 'choices' in response and len(response['choices']) > 0:
                    conversation.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
                else:
                    raise Exception("No response from OpenAI API")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

def print_conversation(conversation: deque) -> None:
    """
    Function to print the conversation
    """
    for message in conversation:
        print(f"{message['role']}: {message['content']}")

class UserInput:
    def __init__(self, master):
        self.master = master
        master.title("Content Creation")
        self.content_type = stringvar(master)
        self.content_type.set("Article")
        self.label = label(master, text="Content Type")
        self.option = optionmenu(master, self.content_type, "Article", "Blog Post", "Short Story")
        self.label2 = label(master, text="Subject Matter")
        self.entry = entry(master)
        self.submit_button = button(master, text="Submit", command=self.submit)
        self.label.pack()
        self.option.pack()
        self.label2.pack()
        self.entry.pack()
        self.submit_button.pack()

    def submit(self):
        content_type = self.content_type.get()
        subject_matter = self.entry.get()
        conversation = initialize_conversation()
        conversation_loop(conversation,content_type, subject_matter)
        print_conversation(conversation)

if __name__ == "__main__":
    root = tk.Tk()
    user_input = UserInput(root)
    root.mainloop()
