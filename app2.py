from flask import Flask, request
import anthropic
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

@app.route("/")
def home():
    return """
    <h1>AI Code Explainer</h1>
    <form action="/explain" method="post">
        <textarea name="code" rows="10" cols="50" placeholder="Paste your code here..."></textarea>
        <br>
        <button type="submit">Explain Code</button>
    </form>
    """
@app.route("/explain", methods=["POST"])
def explain():
    user_input = request.form["code"]
    
    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=4096,
        system="You are a coding assistant that gives simple and understandable explanations for each line of code given to you.",
        messages=[
            {"role": "user", "content": user_input}
        ]
    )
    
    explanation = message.content[0].text
    return f"<h2>Explanation:</h2><pre>{explanation}</pre>"
app.run(debug=True, port=8080)