import flask as f
import os
import pysolr
import bs4
from url_normalize import url_normalize as urlnorm
import urllib.request
from dotenv import load_dotenv
import flask_login
from pymongo import MongoClient

load_dotenv()
if os.environ.get("OWDEX_DEVMODE"): print("Running Owdex in development mode!")

app = f.Flask(__name__)
app.secret_key = os.environ.get("secret_key")

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

users = {'foo@bar.tld': {'password': 'secret'}}


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email
    return user


solr_prefix = "http://solr:8983/solr/" if not os.environ.get(
    "OWDEX_DEVMODE") else "http://localhost:8983/solr/"
dbs = {
    db_name: pysolr.Solr(solr_prefix + db_name)
    for db_name in ["stable", "unstable", "archive"]
}

mongo_client = MongoClient("mongodb://mongo:27017/" if not os.environ.get(
    "OWDEX_DEVMODE") else "mongodb://localhost:27017")

user_db = mongo_client["users"]
user_cl = user_db["users"]

user_cl.insert_one({"name": "alex", "phrase": "hi!", "age": 17})

cursor = user_cl.find()
for record in cursor:
    print(record)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if f.request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               '''

    email = f.request.form['email']
    if email in users and f.request.form['password'] == users[email][
            'password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return f.redirect(f.url_for('protected'))

    return 'Bad login'


@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized', 401


@app.route("/")
def home():
    return f.render_template("home.html")


@app.route("/add", methods=["GET", "POST"])
def add():
    if f.request.method == "POST":
        url = urlnorm(f.request.form["url"])
        title = f.request.form["title"]
        submitter = f.request.form["submitter"]

        with urllib.request.urlopen(url) as response:
            soup = bs4.BeautifulSoup(response.read(), features="html.parser")
            content = soup.get_text()
            description = soup.find("meta", attrs={"name": "description"})
            if description:
                description = description.get("content")

        dbs["unstable"].add(
            {
                "url": url,
                "title": title,
                "description": description,
                "submitter": submitter,
                "content": content
            },
            commit=True)
        return f.render_template("add.html")

    else:
        return f.render_template("add.html")


@app.route("/about")
def about():
    return f.render_template("about.html")


@app.route("/ping")
def ping():
    if os.environ.get("OWDEX_DEVMODE"):
        return dbs["stable"].ping()
    else:
        return "Not in development mode, ping not allowed!"


@app.route("/search")
def search():
    query = f.request.args.get('query')
    indices = f.request.args.getlist('index')
    sort = f.request.args.get('sort')

    results = dbs["unstable"].search(query)

    return f.render_template("search.html",
                             query=query,
                             indices=indices,
                             sort=sort,
                             results=results)


if __name__ == '__main__':
    if os.environ.get("OWDEX_DEVMODE"):
        app.run(host="127.0.0.1", port="5000", debug=True)
    else:
        from waitress import serve
        port = int(os.environ.get('PORT', 80))
        serve(app, host='0.0.0.0', port=port)
