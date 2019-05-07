from flask import Flask, request, make_response, render_template

app = Flask(__name__)


@app.route('/',methods=['get','post'])
def hello_world():
    param_kleur = request.form.get("kleur")
    if param_kleur==None: param_kleur="green"
    #resp = make_response(render_template('myTemplate.html',kleur = param_kleur))
    return "Hello World!"


if __name__ == '__main__':
    app.run()
