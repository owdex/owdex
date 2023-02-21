import flask as f

app = f.Flask(__name__)

@app.route("/")
def home():
    return f.render_template("home.html")