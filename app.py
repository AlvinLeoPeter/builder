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
    <textarea id="code" rows="10" cols="50" placeholder="Paste your code here..."></textarea>
    <br>
    <button>Explain Code</button>
    """

app.run(debug=True, port=8080)