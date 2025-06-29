from ollama import Client


# Connect to the local Ollama server
client = Client(host='http://localhost:11434')

# Send a prompt to the model
response = client.chat(
    model='llama3.2:latest', 
    messages=[
        {
            "role": "user", 
            "content": "Who is the current president of Indonesia?"
        }
    ]
)

# Print the model's response
print(response['message']['content'])