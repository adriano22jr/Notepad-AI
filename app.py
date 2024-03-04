import flask, requests, app_config
import scripts.db_functions as db_functions
import scripts.container_operations as container_ops

app = flask.Flask(__name__, template_folder = "templateFiles", static_folder = "staticFiles")

app.secret_key = app_config.APP_SECRET_KEY
client_id = app_config.GOOGLE_CLIENT_ID
client_config = app_config.GOOGLE_CLIENT_SECRET


@app.route("/", methods = ["GET", "POST"])
def index():
    try:
        if flask.session["logged"] == True:
            session_user = flask.session["session-user"]
            notebooks = db_functions.find_user_notebooks(session_user["UserID"])
            return flask.render_template("index.html", notebooks = notebooks, lenght = len(notebooks))
        else: return flask.render_template("index.html")
    except:
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
    user = flask.session["session-user"]
    if email == user["Email"]:
        db_functions.delete_user(email)
        flask.session.clear()
        status_code = flask.Response(status = 200)
    else: status_code = flask.Response(status = 400)
    return status_code

@app.route("/delete-notebook", methods = ["POST"])
def delete_notebook():
    notebook_id = flask.request.form.get("notebook_id")
    notebook = db_functions.get_notebook(notebook_id)
    
    db_functions.delete_notebook(notebook_id)
    container_ops.delete_text_blob(notebook["StoredNotebookName"])
    status_code = flask.Response(status = 200)
    return status_code

@app.route("/redirect-notebook", methods = ["POST"])
def redirect_notebook():
    flask.session["notebook_name"] = flask.request.form.get("notebook_name")
    status_code = flask.Response(status = 200)
    return status_code

@app.route("/notebook-regular", methods = ["GET", "POST"])
def notebook_regular():
    return flask.render_template("notebook_regular.html")

@app.route("/notebook-markdown", methods = ["GET", "POST"])
def notebook_markdown():
    return flask.render_template("notebook_markdown.html")



if __name__ == "__main__":
    app.run(port = 8080, debug=True)