import flask as f

app = f.Flask(__name__)

@app.route("/")
def home():
    return f.render_template("home.html")

@app.route("/search")
def search():
    q = f.request.args.get('q')
    index = f.request.args.getlist('index')
    sort = f.request.args.get('sort')
    return f"Query: {q}\nIndices:{index}\nSort:{sort}"