from flask import Flask
from web_client.config import Config
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.config.from_object(Config)

import web_client.gender_equality_client.views