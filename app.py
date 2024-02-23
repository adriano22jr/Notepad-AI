import flask, os
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from pip._vendor import cachecontrol
import google.auth.transport.requests

app = flask.Flask(__name__, template_folder = "templateFiles", static_folder = "staticFiles")
app.secret_key = 'notepadai'
client_id = os.environ["GOOGLE_CLIENT_ID"]
client_config = os.environ["GOOGLE_PROVIDER_AUTHENTICATION_SECRET"]

flow = Flow.from_client_config(client_config = client_config, 
                               scopes = ["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
                               redirect_uri = "http://127.0.0.1:8080/callback")

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

@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    flask.session["state"] = state
    return flask.redirect(authorization_url)

@app.route("/logout")
def logout():
    flask.session.clear()
    return flask.render_template("index.html")

@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response = flask.request.url)

    if not flask.session["state"] == flask.request.args["state"]:
        flask.abort(500)
    
    credentials = flow.credentials
    request_session = flask.request.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session = cached_session)
    
    id_info = id_token.verify_oauth2_token(
        id_token = credentials.id_token,
        request = token_request,
        audience = client_id
    )
    
    flask.session["google_id"] = id_info.get("sub")
    flask.session["profile_name"] = id_info.get("name")
    flask.session["logged"] = True
    return flask.render_template("index.html")


@app.route("/notebook-regular", methods = ["GET", "POST"])
@login_required
def notebook_regular():
    return flask.render_template("notebook_regular.html")

@app.route("/notebook-markdown", methods = ["GET", "POST"])
@login_required
def notebook_markdown():
    return flask.render_template("notebook_markdown.html")

if __name__ == "__main__":
    app.run(port = 8080, debug=True)