from instruments import app
app.config.from_object('settings') #rename settings.cfg settings.py

app.load_blueprints()

app.run(host='0.0.0.0', debug=True)