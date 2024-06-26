import flask, requests, markdown, app_config, ast, pdfkit, os
import scripts.db_functions as db_functions
import scripts.container_operations as container_ops
import scripts.ai_services as ai_services

app = flask.Flask(__name__, template_folder = "templateFiles", static_folder = "staticFiles")
os.system("apt-get install -y wkhtmltopdf")

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
    
@app.route("/services", methods = ["GET", "POST"])
def services():
    return flask.render_template("services.html")

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

@app.route("/notebook-regular/<name>", methods = ["POST"])
def notebook_regular(name):
    user_notebooks = db_functions.find_user_notebooks(flask.session["session-user"]["UserID"])
    notebook = db_functions.get_notebook_by_title(name)
    if notebook is not None:
        stored_content = ast.literal_eval(container_ops.get_blob_content(notebook["StoredNotebookName"]))
        content = ""
        for elem in stored_content:
            content += "<div>" + elem + "</div>"
        return flask.render_template("notebook_regular.html", notebook_title = name, notebook_name = notebook["StoredNotebookName"], notebook_content = content, notebooks = user_notebooks)
    return flask.render_template("notebook_regular.html", notebook_title = name, notebook_name = "", notebook_content = "", notebooks = user_notebooks)

@app.route("/notebook-markdown/<name>", methods = ["POST"])
def notebook_markdown(name):
    user_notebooks = db_functions.find_user_notebooks(flask.session["session-user"]["UserID"])
    notebook = db_functions.get_notebook_by_title(name)
    if notebook is not None:
        content = container_ops.get_blob_content(notebook["StoredNotebookName"])
        return flask.render_template("notebook_markdown.html", notebook_title = name, notebook_name = notebook["StoredNotebookName"], notebook_content = content, notebooks = user_notebooks)
    return flask.render_template("notebook_markdown.html", notebook_title = name, notebook_name = "", notebook_content = "", notebooks = user_notebooks)

@app.route("/delete-account", methods = ["POST"])
def delete_account():
    email = flask.request.form.get("email")
    user = flask.session["session-user"]
    if email == user["Email"]:
        notebooks = db_functions.find_user_notebooks(user["UserID"])
        for note in notebooks:
            container_ops.delete_text_blob(note["StoredNotebookName"])
            
        db_functions.delete_user(email)
        flask.session.clear()
        status_code = flask.Response(status = 200)
    else: status_code = flask.Response(status = 400)
    return status_code

@app.route("/new", methods = ["POST"])
def new_notebook():
    notebook_name = flask.request.form["notebook-name"]
    notebook_type = flask.request.form["inlineRadioOptions"]
    
    if notebook_type == "regular": return flask.redirect(flask.url_for('notebook_regular', name = notebook_name), code = 307)
    elif notebook_type == "markdown": return flask.redirect(flask.url_for('notebook_markdown', name = notebook_name), code = 307)
    else: return flask.Response(status = 404)
    
@app.route("/open-notebook", methods = ["POST"])
def open_notebook():
    notebook_id = flask.request.form["notebook-id"]
    notebook = db_functions.get_notebook_by_id(int(notebook_id))
    
    if notebook["NotebookType"] == "regular":
        return flask.redirect(flask.url_for('notebook_regular', name = notebook["NotebookTitle"]), code = 307)
    elif notebook["NotebookType"] == "markdown": return flask.redirect(flask.url_for('notebook_markdown', name = notebook["NotebookTitle"]), code = 307)
    else: return flask.Response(status = 404)
    
@app.route("/save-notebook", methods = ["POST"])
def save_notebook():
    notebook_title = flask.request.form.get("notebook_title")
    notebook_name = flask.request.form.get("notebook_name")
    notebook_content = flask.request.form.get("notebook_content")
    notebook_type = flask.request.form.get("notebook_type")
    user = flask.session["session-user"]
    
    rows = notebook_content.split("<div>")
    strings = []
    for row in rows: 
        elem = row.replace("</div>", "")
        strings.append(elem)    
    
    notebook = db_functions.get_notebook_by_stored_name(notebook_name)
    if notebook is None:
        db_functions.insert_notebook(notebook_title, user["UserID"], user["Email"], notebook_type)
        if notebook_type == "regular": container_ops.upload_new_text_blob(f"{notebook_title}-{user["Email"]}", str(strings))
        else: container_ops.upload_new_text_blob(f"{notebook_title}-{user["Email"]}", notebook_content)
    else:
        if notebook_title == notebook["NotebookTitle"]:
            if notebook_type == "regular": container_ops.update_text_blob(notebook["StoredNotebookName"], str(strings))
            else: container_ops.update_text_blob(notebook["StoredNotebookName"], notebook_content)
        else:
            db_functions.update_notebook_title(notebook_title, notebook["NotebookID"])
            if notebook_type == "regular": container_ops.update_text_blob(notebook["StoredNotebookName"], str(strings))
            else: container_ops.update_text_blob(notebook["StoredNotebookName"], notebook_content)
            
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

@app.route("/render-markdown", methods = ["POST"])
def render_markdown():
     notebook_content = flask.request.form.get("notebook_content")
     markdown_content = markdown.markdown(notebook_content)
     return flask.jsonify({"content": markdown_content}), 200

@app.route("/summarize-text", methods = ["POST"])
def summarize_text():
    text_to_summarize = flask.request.form.get("text-to-summarize")
    summarized_text = ai_services.extract_summarization([str(text_to_summarize)])
    
    text_translator_data = ai_services.detect_language(str(text_to_summarize))
    text_language_detected = text_translator_data[0]["language"]
    
    if text_language_detected != "en":
        translation_data = ai_services.translate_text(summarized_text, [text_language_detected])  
        translated_summarization = translation_data[0]["translations"][0]["text"]
        return flask.jsonify({"summarization": translated_summarization})
    else: return flask.jsonify({"summarization": summarized_text})

@app.route("/translate-text", methods = ["POST"])
def translate_text():
    text_to_translate = flask.request.form.get("text-to-translate")
    language_code = flask.request.form.get("language_code")
    
    translation_data = ai_services.translate_text(text_to_translate, [language_code])  
    translated_text = translation_data[0]["translations"][0]["text"]
    return flask.jsonify({"translation": translated_text})

@app.route("/get-speech", methods = ["POST"])
def get_speech():
    language_code = flask.request.form.get("language_code")
    
    recognized = ai_services.recognize_speech(language_code)
    return flask.jsonify({"recognized_speech": recognized})

@app.route("/generate-text", methods = ["POST"])
def generate_text():
    input_text = flask.request.form.get("input_text")
    
    generation = ai_services.generate_text(str(input_text))
    return flask.jsonify({"generation": generation})

@app.route("/download-content", methods = ["POST", "GET"])
def download_content():
    notebook_title = flask.request.form["notebook-title"]
    notebook = db_functions.get_notebook_by_title(notebook_title)
    
    if notebook["NotebookType"] == "regular": 
        stored_content = ast.literal_eval(container_ops.get_blob_content(notebook["StoredNotebookName"]))
        content = ""
        for elem in stored_content:
            content += "<div>" + elem + "</div>" 
    else: 
        content = container_ops.get_blob_content(notebook["StoredNotebookName"])
    markdown_content = markdown.markdown(content)
    
    response_string = pdfkit.from_string(markdown_content, False)
    response = flask.make_response(response_string)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline;filename=" + notebook_title + ".pdf"
    return response

if __name__ == "__main__":
    app.run(port = 8080, debug = True)