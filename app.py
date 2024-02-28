import flask, requests, app_config
import scripts.db_functions as db_functions

app = flask.Flask(__name__, template_folder = "templateFiles", static_folder = "staticFiles")

app.secret_key = app_config.APP_SECRET_KEY
client_id = app_config.GOOGLE_CLIENT_ID
client_config = app_config.GOOGLE_CLIENT_SECRET


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
    
    res = db_functions.check_exising_user(str(data["email"]))
    if res is None:
        db_functions.insert_user(str(data["given_name"]), str(data["family_name"]), str(data["email"]), str(data["name"]))
        session_user = db_functions.check_exising_user(str(data["email"]))
        flask.session["session-user"] = session_user
    else:
        flask.session["session-user"] = res
        
    flask.session["logged"] = True
    flask.session["profile_name"] = data["name"]
    return flask.redirect(flask.url_for('index'))

@app.route("/delete-account", methods = ["POST"])
def delete_account():
    email = flask.request.form.get("email")
    if email == flask.session["session-user"]["email"]:
        flask.response.status_code = 200
    else: flask.response.status_code = 400
    return flask.response



@app.route("/notebook-regular", methods = ["GET", "POST"])
def notebook_regular():
    return flask.render_template("notebook_regular.html")

@app.route("/notebook-markdown", methods = ["GET", "POST"])
def notebook_markdown():
    return flask.render_template("notebook_markdown.html")



if __name__ == "__main__":
    app.run(port = 8080, debug=True)