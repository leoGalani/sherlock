"""Flask Main Project File."""
from flask import Flask
from sherlock.controllers.users import user


app = Flask(__name__)

app.register_blueprint(user, url_prefix='/user')
