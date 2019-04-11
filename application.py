"""
(c)HAN University of Appliec Science/Martijn van der Bruggen
Voorbeeld van een web applicatie
Een eerste aanzet
Creatie d.d. 1 april 2019
"""

from flask import Flask
from flask import render_template, request
import mysql.connector
from Bio.Seq import Seq

app = Flask(__name__)

"""
Default functie om een HTML pagina te renderen
"""


@app.route("/")
def hello():
    return render_template('index.html')


"""
Mogelijkheid om te zoeken naar een woord in de ensembl database
Parameter overdracht middels de get methode
"""


@app.route("/sql")
def sqldemo():
    woord = request.args.get('woord')
    if woord==None:
        woord = "zinc"

    verbinding = mysql.connector.connect(host="ensembldb.ensembl.org",
                                         user="anonymous",
                                         db="homo_sapiens_core_95_38")
    cursor = verbinding.cursor()
    cursor.execute("select * from gene where description like '%{}%' limit 10".format(woord))
    regel = ""
    tekst = """<form method="get">
    <input type="text" name="woord" value="zinc">
    <input type="submit" value="Submit">
    </form><hr>"""
    while regel != None:
        if len(regel) > 9:
            tekst += str(regel[9]).replace(woord, "" + woord + "") + "<br>"

        regel = cursor.fetchone()

    cursor.close()
    verbinding.close()

    return tekst


"""
Mogelijkheid om te zoeken in de studenten database
Parameter overdracht met de post method
"""


@app.route("/piep")
def piepapp():
    hostname = "hannl-hlo-bioinformatica-mysqlsrv.mysql.database.azure.com"
    woord = request.form.get('woord')
    tekst = ""
    wachtwoord = request.form.get('ww')
    if woord == None:
        woord = ""
    if wachtwoord == None:
        wachtwoord = ""
    tekst = """<form method="post">
             Gebruiker : <input type="text" name="gebruiker"></input><br>
             Wachtwoord: <input type="password" name="ww" value={}></input><br><hr>
             Zoekwoord : <input type="text" name="woord" value="">
             <input type="submit" value="Submit"
             </form><hr>""".format(wachtwoord)

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
    try:
        conn = mysql.connector.connect(host=hostname,
                                       user="dummy@" + hostname,
                                       passwd=wachtwoord)
        cursor = conn.cursor()
        cursor.execute("use dummy")
        cursor.execute(query)

        for bericht in cursor:
            tekst += "<b>" + bericht[0] + "</b>"
            tekst += "<i>" + str(bericht[2]) + ' ' + bericht[3] + "</i><br>"
            tekst += bericht[1] + "<br>"
        cursor.close()
        conn.close()
    except:
        tekst += "Er gaat iets mis met de database connectie"
    return tekst

@app.route("/bio")
def convert():
    pass
