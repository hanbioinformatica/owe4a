from flask import Flask
from flask import render_template
import mysql.connector

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/sql")
def piep():
    woord = "zinc"
    verbinding = mysql.connector.connect(host="ensembldb.ensembl.org",
                                         user="anonymous",
                                         db="homo_sapiens_core_95_38")
    cursor = verbinding.cursor()
    cursor.execute("select * from gene where description like '%{}%' limit 10".format(woord))
    regel = ""
    tekst = ""
    while regel != None:
        if len(regel)>9:
            tekst += str(regel[9]) + "<br>"
        regel = cursor.fetchone()

    cursor.close()
    verbinding.close()

    return tekst



