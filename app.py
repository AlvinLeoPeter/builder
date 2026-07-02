from database import init_db, save_explanation, get_history
from flask import Flask, request
import anthropic
from dotenv import load_dotenv
import os
import markdown

load_dotenv()

app = Flask(__name__)
init_db()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Code Explainer</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
        <style>
            body {
                background-color: #1e1e1e;
                color: #ffffff;
                font-family: Arial, sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                margin: 0;
                padding: 20px;
            }
            h1 { color: #61dafb; }
            textarea {
                width: 600px;
                height: 200px;
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                resize: vertical;
            }
            button {
                margin-top: 10px;
                padding: 10px 30px;
                background-color: #61dafb;
                color: #1e1e1e;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                cursor: pointer;
                font-weight: bold;
            }
            button:hover { background-color: #21a1cb; }
            #result {
                margin-top: 20px;
                width: 600px;
                background-color: #2d2d2d;
                border-radius: 8px;
                padding: 20px;
                display: none;
            }
        </style>
    </head>
    <body>
        <h1>🧠 AI Code Explainer</h1>
        <p style="color: #888;">Paste your code and get a simple explanation instantly.</p>
        <a href="/history" style="color: #61dafb; font-size: 14px;">📚 View History</a>
        <form id="codeForm">
            <textarea name="code" id="codeInput" placeholder="Paste your code here..."></textarea>
            <br>
            <button type="submit">Explain Code ✨</button>
        </form>
        <div id="result">
            <h3 style="color: #61dafb;">Explanation:</h3>
            <pre id="explanation" style="white-space: pre-wrap; color: #ddd;"></pre>
        </div>
        <script>
            document.getElementById('codeForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                const code = document.getElementById('codeInput').value;
                const result = document.getElementById('result');
                const explanation = document.getElementById('explanation');
                explanation.textContent = 'Explaining...';
                result.style.display = 'block';
                const response = await fetch('/explain', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: 'code=' + encodeURIComponent(code)
                });
                const text = await response.text();
                explanation.innerHTML = text;
                document.querySelectorAll('pre code').forEach((block) => {
                hljs.highlightElement(block);
                });
            });
        </script>
    </body>
    </html>
    """

@app.route("/explain", methods=["POST"])
def explain():
    user_input = request.form["code"]
    
    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=4096,
        system="You are a coding assistant that gives simple and understandable explanations for each line of code given to you. Only put actual code in code blocks. Never put URLs, brackets, or punctuation in code blocks.",
        messages=[
            {"role": "user", "content": user_input}
        ]
    )
    
    explanation_md = message.content[0].text
    explanation_html = markdown.markdown(explanation_md, extensions=['fenced_code'])
    save_explanation(user_input, explanation_md)
    return explanation_html

@app.route("/history")
def history():
    records = get_history()
    html = """
    <html>
    <head>
        <style>
            body { background-color: #1e1e1e; color: #fff; 
                   font-family: Arial; padding: 20px; }
            .entry { background: #2d2d2d; border-radius: 8px; 
                     padding: 15px; margin-bottom: 15px; }
            .timestamp { color: #888; font-size: 12px; }
            .code { background: #111; padding: 10px; 
                    border-radius: 5px; margin: 10px 0; }
            a { color: #61dafb; }
        </style>
    </head>
    <body>
        <h1>📚 Explanation History</h1>
        <a href="/">← Back to Explainer</a>
        <br><br>
    """
    for record in records:
        html += f"""
        <div class="entry">
            <div class="timestamp">🕐 {record[3]}</div>
            <div class="code"><pre>{record[1]}</pre></div>
            <p id="preview-{record[0]}">{markdown.markdown(record[2][:200], extensions=['fenced_code'])}... 
    <button onclick="document.getElementById('full-{record[0]}').style.display='block';
                 document.getElementById('preview-{record[0]}').style.display='none';" 
        style="background:#61dafb;border:none;padding:5px 10px;border-radius:5px;
               cursor:pointer;color:#1e1e1e;font-weight:bold;">
    Show More
    </button>
</p>
<div id="full-{record[0]}" style="display:none;">
    {markdown.markdown(record[2], extensions=['fenced_code'])}
    <button onclick="document.getElementById('full-{record[0]}').style.display='none';
                     document.getElementById('preview-{record[0]}').style.display='block';"
            style="background:#444;border:none;padding:5px 10px;border-radius:5px;
                   cursor:pointer;color:#fff;font-weight:bold;margin-top:10px;">
        Show Less
    </button>
</div>
        </div>
        """
    html += "</body></html>"
    return html

app.run(debug=True, port=8080)