import anthropic
from dotenv import load_dotenv
import os

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

while True:

    user_input = input("Paste your code here: type 'exit' to quit:")

    if user_input == "exit":
        break

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=4096,
        system="You are a coding assistant that gives simple and understandable answers to each line of the code given to you.",
        messages=[
        {"role": "user", "content": user_input}
        ]

    )
    print(message.content[0].text)

    

