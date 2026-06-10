from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>AI Code Explainer</h1>
    <p>Paste your code and get a simple explanation.</p>
    """

app.run(debug=True, port=8080)