from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello DEMO!"

@app.route("/show")
def hello():
    return "<body bg="red">Hello DEMO!"
