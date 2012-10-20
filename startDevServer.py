from instruments import app

app.config.from_pyfile('../settings.cfg')
app.run(host='0.0.0.0', debug=True)