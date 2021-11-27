from flask import Flask
from .app import app


#config Variables should be hidden from end user
app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
app.config['MAIL_PORT'] =587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_DEFAULT_SENDER'] = ''
app.config["GITHUB_OAUTH_CLIENT_ID"]=''
app.config["GITHUB_OAUTH_CLIENT_SECRET"]=''
app.config["GOOGLE_OAUTH_CLIENT_ID"]=""
app.config["GOOGLE_OAUTH_CLIENT_SECRET"]=""
