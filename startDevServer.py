from instruments import app
app.config.from_object('settings')

app.run(host='0.0.0.0', debug=True)