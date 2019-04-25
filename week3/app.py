from flask import Flask, request

app = Flask(__name__)


@app.route('/demo',methods=['get','post'])
def hello_world():
    param_kleur = request.form.get("kleur")
    if param_kleur==None: param_kleur="green"
    return '''<head><link rel="stylesheet" href="https://unpkg.com/picnic"></head><body bgcolor="{}">Hello World! 
    <form method="post">
    <br>Kleur:<input type="text" name="kleur"><br>
    Username: <input type="text" name="username"><br>
    Wachtwoord: <input type="password" name="wachtwoord"><br>
    <input type="submit" value="klik">
    </form>
    '''.format(param_kleur)


@app.route('/')
def hello_world2():
    return "dit is de start"


if __name__ == '__main__':
    app.run()
