import openai
import os
import json
import logging 
from collections import deque
from dotenv import load_dotenv 
from typing import Deque 

# Load environment variables from .env file
load_dotenv() 

# Set up logging
logging.basicConfig(level=logging.INFO) 

# Load the OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY', 'default_value') 

if openai.api_key is 'default_value':
    logging.error("OPENAI_API_KEY is not set in the environment variables.")
    exit(1) 

# Define the chat models
chat_model = "gpt-3.5-turbo" 

# Define the system roles from text files
def read_file(file_name: str) -> str:
    try:
        with open(file_name, 'r') as file:
            return file.read().replace('\n', '')
    except (FileNotFoundError, PermissionError, IsADirectoryError, IOError) as e:
        logging.error(f"Error reading {file_name}: {e}")
        return '' 

chatbot1_role = read_file('Mrs_Writer.txt')
chatbot2_role = read_file('Mr_Editor.txt') 

# Initialize the conversation
def initialize_conversation() -> Deque:
    conversation = deque()
    conversation.append({"role": "system", "content": f"I'm a helpful assistant. {chatbot1_role}"})
    conversation.append({"role": "system", "content": f"I'm a helpful assistant. {chatbot2_role}"})
    return conversation 

# Define the conversation loop
def conversation_loop(conversation: Deque) -> None:
    try:
        for i in range(10):
            for chatbot_role in [(chatbot1_role, "Mrs Writer"), (chatbot2_role, "Mr Editor")]:
                message = {"role": "user", "content": f"{chatbot_role[1]}'s turn. {chatbot_role[0]}"}
             conversation.append(message)
                response = openai.ChatCompletion.create(model=chat_model, messages=list(conversation), timeout=10)
                conversation.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
    except Exception as e        logging.error(f"An error occurred: {e}") 

# Print the conversation
def print_conversation(conversation: Deque) -> None:
    for message in conversation:
        print(f"{message['role']}: {message['content']}") 

# Main function to run the conversation
def main() -> None:
    conversation = initialize_conversation()
    conversation_loop(conversation)
    print_conversation(conversation) 

if __name__ == "__main__":
    main()
