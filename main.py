import gradio as gr
import requests
import json

# Define a global variable for the conversation history
conversation_history = ""

def chat_with_ai(user_question, api_key, model):
    global conversation_history

    # Instantiate the endpoint URL
    url = 'https://api.anthropic.com/v1/complete'

    # Define the headers for the HTTP request
    headers = {
        'Content-Type': 'application/json',
        'X-API-Key': api_key,
    }

    # Define the parameters for the request
    params = {
        'prompt': f'{conversation_history}\n\nHuman: {user_question}\n\nAssistant:',
        'model': model,
        'max_tokens_to_sample': 4000,
        'stop_sequences': ['\n\nHuman:'],
        'temperature': 0.8,
        'top_p': -1,
        'metadata': {}
    }

    # Convert the params dict to a JSON string
    params_json = json.dumps(params)

    # Send the HTTP request to the API
    response = requests.post(url, headers=headers, data=params_json)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        response_json = response.json()
        conversation_history += f'\n\nHuman: {user_question}\n\nAssistant: {response_json["completion"]}'

        # Return the entire conversation history
        return conversation_history
    else:
        return f'Error: {response.status_code}'

# Define the model options
model_options = ["claude-v1", "claude-v1-100k", "claude-v1.0", "claude-v1.2", "claude-v1.3", "claude-v1.3-100k", "claude-instant-v1", "claude-instant-v1-100k", "claude-instant-v1.0", "claude-instant-v1.1", "claude-instant-v1.1-100k"]

iface = gr.Interface(fn=chat_with_ai, 
                     inputs=["text", "text", gr.Dropdown(model_options)], 
                     outputs="text",
                     layout="vertical")
iface.launch()
