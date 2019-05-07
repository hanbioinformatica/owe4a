from flask import Flask, request, make_response, render_template

app = Flask(__name__)


@app.route('/', methods=['get', 'post'])
def hello_world():
    param_kleur = request.form.get("kleur")
    if param_kleur == None: param_kleur = "green"
    resp = """<body bgcolor="{}">Hello World!
    <form method="post">
    <br>Kleur:<input type="text" name="kleur"><br>
    Username: <input type="text" name="username"><br>
    Wachtwoord: <input type="password" name="wachtwoord"><br>
    <input type="submit" value="klik">
    </form>
    </body>""".format(param_kleur)
    return resp


if __name__ == '__main__':
    app.run()
