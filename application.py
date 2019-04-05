from flask import Flask
from flask import render_template, request
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
        if len(regel) > 9:
            tekst += str(regel[9]) + "<br>"
        regel = cursor.fetchone()

    cursor.close()
    verbinding.close()

    return tekst


@app.route("/piep")
def piepapp():
    hostname = "hannl-hlo-bioinformatica-mysqlsrv.mysql.database.azure.com"
    woord = ""
    tekst = ""
    wachtwoord = request.args.get('ww')
    query = "select voornaam, " \
            " bericht, " \
            " if(datum!=curdate(),datum,'vandaag ') datum," \
            " if(datum!=curdate(),tijd, concat(convert(timediff(curtime(),tijd), char),' geleden')) tijd," \
            " timestamp(datum,tijd) datumtijd" \
            " from student " \
            " natural join piep " \
            " where bericht like '%{}%'" \
            " order by datumtijd desc" \
            " limit 100 ".format(woord)

    conn = mysql.connector.connect(host=hostname,
                                   user="dummy@" + hostname,
                                   passwd=wachtwoord)
    cursor = conn.cursor()
    cursor.execute("use dummy")
    cursor.execute(query)

    for bericht in cursor:
        tekst += bericht[0]+"<br>"
        tekst += str(bericht[2]) + ' ' + bericht[3]+"<br>"
        tekst += bericht[1]+"<br>"
    cursor.close()
    conn.close()
    return tekst