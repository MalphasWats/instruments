from flask import Flask

app = Flask(__name__)
app.config.from_object('settings')

import core
core.load_blueprints()

