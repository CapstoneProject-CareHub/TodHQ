import openai
import os
import time
import re

from dotenv import load_dotenv
load_dotenv() # Load environment variables from .env file

openai.api_key = os.getenv('OPENAI_API_KEY')

client = openai.Client()

# def create_assistant():
#     assistant = client.beta.assistants.create(
#         instructions="You are a customer support chatbot. Use your knowledge base to best respond to customer queries.",
#         model="gpt-3.5-turbo-1106",
#         tools=[{"type": "retrieval"}],
#         file_ids=["file-rHWIVEWDLS7Yr3lzZdYlGKVS"]
#     )
#     return assistant.id  # Return the assistant ID

def remove_citation(text):
    # Regex pattern to find and remove citation like &#8203;``【oaicite:1】``&#8203;
    pattern = r"&#8203;``【oaicite:0】``&#8203;"
    return re.sub(pattern, "", text)

def get_response(user_message, assistant_id):
    thread = client.beta.threads.create()

    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_message,
        file_ids=["file-ltnFKp9YDWJu1WFFJ6GOd44m"]
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
        instructions="Please address the user's question. Use the knowledge base to help you answer the question."
    )

    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if run_status.status in ["completed", "failed"]:
            break
        time.sleep(5)

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    print(messages)
    if messages and messages.data:
        for message in messages.data:
            if message.role == 'assistant':
                if isinstance(message.content, list):
                    for content in message.content:
                        if hasattr(content, 'text') and hasattr(content.text, 'value'):
                            response = content.text.value
                            response = remove_citation(response)  # Remove citation from response
                            print(response)
                            return response
                else:
                    return "Response format not recognized"

    return "I'm sorry, I couldn't find an answer."