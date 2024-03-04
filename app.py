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

@app.route("/notebook-regular/<name>", methods = ["GET", "POST"])
def notebook_regular(name):
    return flask.render_template("notebook_regular.html", notebook_name = name, notebook_content = "")

@app.route("/notebook-markdown/<name>", methods = ["GET", "POST"])
def notebook_markdown(name):
    return flask.render_template("notebook_markdown.html", notebook_name = name, notebook_content = "")

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

@app.route("/save-notebook", methods = ["POST"])
def save_notebook():
    notebook_title = flask.request.form.get("notebook_title")
    notebook_content = flask.request.form.get("notebook_content")
    notebook_type = flask.request.form.get("notebook_type")
    user = flask.session["session-user"]
    
    notebook = db_functions.get_notebook_by_title(notebook_title)
    if notebook is None:
        db_functions.insert_notebook(notebook_title, user["UserID"], user["Email"], notebook_type)
        container_ops.upload_new_text_blob(f"{notebook_title}-{user["Email"]}", notebook_content)
    else:
        container_ops.update_text_blob(notebook["StoredNotebookName"], notebook_content)
    
    status_code = flask.Response(status = 200)
    return status_code

@app.route("/delete-notebook", methods = ["POST"])
def delete_notebook():
    notebook_id = flask.request.form.get("notebook_id")
    notebook = db_functions.get_notebook_by_id(int(notebook_id))
    
    db_functions.delete_notebook(notebook_id)
    container_ops.delete_text_blob(notebook["StoredNotebookName"])
    status_code = flask.Response(status = 200)
    return status_code

@app.route("/open-notebook", methods = ["POST"])
def open_notebook():
    notebook_id = flask.request.form.get("notebook_id")
    notebook = db_functions.get_notebook_by_id(int(notebook_id))
    content = container_ops.get_blob_content(notebook["StoredNotebookName"])
    
    return flask.jsonify({"content": content}), 200


if __name__ == "__main__":
    app.run(port = 8080, debug=True)