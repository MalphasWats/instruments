from flask import Flask

app = Flask(__name__)

import core
app.load_blueprints = core.load_blueprints

