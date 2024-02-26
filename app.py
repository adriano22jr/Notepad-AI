import flask, requests, app_config

app = flask.Flask(__name__, template_folder = "templateFiles", static_folder = "staticFiles")

app.secret_key = app_config.APP_SECRET_KEY
client_id = app_config.GOOGLE_CLIENT_ID
client_config = app_config.GOOGLE_CLIENT_SECRET

def login_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in flask.session:
            return flask.abort(401)
        else:
            return function()
    return wrapper


@app.route("/", methods = ["GET", "POST"])
def index():
    return flask.render_template("index.html")

@app.route("/logout")
def logout():
    flask.session.clear()
    return flask.render_template("index.html")


@app.route("/callback")
def callback():
    token = flask.request.headers.get("X-MS-TOKEN-GOOGLE-ACCESS-TOKEN")

    data = requests.get(
        "https://openidconnect.googleapis.com/v1/userinfo",
        headers={ 'Authorization': f"Bearer {token}" },
    ).json()
    
    flask.session["logged"] = True
    print(data)
    return flask.render_template("index.html", client_id = data)


@app.route("/notebook-regular", methods = ["GET", "POST"])
def notebook_regular():
    return flask.render_template("notebook_regular.html")

@app.route("/notebook-markdown", methods = ["GET", "POST"])
def notebook_markdown():
    return flask.render_template("notebook_markdown.html")



if __name__ == "__main__":
    app.run(port = 8080, debug=True)