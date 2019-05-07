from flask import Flask, request, make_response, render_template

app = Flask(__name__)


@app.route('/',methods=['get','post'])
def hello_world():
    param_kleur = request.form.get("kleur")
    if param_kleur==None: param_kleur="green"
    return "<marquee>Hello Bioinformatica!</marquee>"


if __name__ == '__main__':
    app.run()
