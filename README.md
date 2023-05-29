
# AgentDuel 

AgentDuel is a Python application that uses OpenAI's GPT-3 model to facilitate a conversation between two AI agents, an Editor and a Writer, with the goal of producing a piece of well-written content. 

## Setup 

1. Clone this repository: 

https://github.com/JackSmack1971/AgentDuel.git 

2. Navigate to the project directory: 

cd AgentDuel 

3. Install the required Python packages: 

pip install -r requirements.txt 

4. Set up your OpenAI API key. Create a `.env` file in the project directory and add your OpenAI API key: 

OPENAI_API_KEY=your_openai_api_key 

Replace `your_openai_api_key` with your actual OpenAI API key. 

## Usage 

Run the `conversationloop.py` script to start the application: 

python conversationloop.py 

A GUI will appear, allowing you to select the type of content (e.g., "Article", "Blog Post", "Short Story") and enter the subject matter. The conversation between the Editor Agent and the Writer Agent will then begin, guided by the content type and subject matter you entered. 

The conversation will continue until the Editor Agent is satisfied with the Writer Agent's content output. The final output will be saved to a text file in the project directory. 

## Content Guidelines 

The `seoarticle.txt` and `content_guidelines.txt` files provide guidelines for the Writer Agent to follow when crafting content. The Editor Agent uses these guidelines to provide feedback and instructions to the Writer Agent. 

- `seoarticle.txt`: Provides guidelines for writing an SEO-friendly article.
- `content_guidelines.txt`: Provides general guidelines for writing any type of content. 

## Contributing 

Contributions are welcome! Please feel free to submit a pull request or open an issue. 

## License 

This project is licensed under the terms of the MIT license.
