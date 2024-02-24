import os

APP_SECRET_KEY = os.environ["FLASK_APP_SECRET_KEY"]
GOOGLE_CLIENT_ID = os.environ["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = os.environ["GOOGLE_PROVIDER_AUTHENTICATION_SECRET"]

nested_rules = {"client_id": {GOOGLE_CLIENT_ID},"project_id":"notepadai","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":{GOOGLE_CLIENT_SECRET},"redirect_uris":["https://notepad-ai.azurewebsites.net/callback"],"javascript_origins":["https://notepad-ai.azurewebsites.net"]}
GOOGLE_APP_SECRETS_FILE = {"web": nested_rules}