import anthropic
from dotenv import load_dotenv
import os

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

user_input = input("Ask me anything: ")

message = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    system="You are a helpful assistant that reponds like a pirate.",
    messages=[
        {"role": "user", "content": user_input}
    ]
)

print(message.content[0].text)