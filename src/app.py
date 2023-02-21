import flask as f

app = f.Flask(__name__)

@app.route("/")
def home():
    return "Hello, World!"