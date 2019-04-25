"""
(c)HAN University of Applied Science/Martijn van der Bruggen
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
Parameteroverdracht middels de get methode (default)
"""
@app.route("/sql")
def sqldemo():
    woord = request.args.get('woord')
    if woord == None: woord = "koe"
    verbinding = mysql.connector.connect(host="ensembldb.ensembl.org",
                                         user="anonymous",
                                         db="homo_sapiens_core_95_38")
    cursor = verbinding.cursor()
    cursor.execute("select * from gene where description like '%{}%' limit 10".format(woord))
    regel = ""
    tekst = """<form method="get">
                <input type="text" name="woord">
                <input type="submit" value="Submit">
                </form>
                <hr>"""
    while regel != None:
        if len(regel) > 9:
            tekst += str(regel[9]).replace(woord, "<b>" + woord + "</b>") + "<br>"
        regel = cursor.fetchone()
    cursor.close()
    verbinding.close()
    return tekst


"""
Mogelijkheid om te zoeken in de studenten database
Parameter overdracht met de post method
Parameters worden dus niet (direct) zichtbaar overgedragen
maar natuurlijk zijn ze wel te achterhalen omdat het verzoek
via een onversleutelde http connectie verloopt
"""


@app.route("/piep", methods=['get', 'post'])
def piepapp():
    hostname = "hannl-hlo-bioinformatica-mysqlsrv.mysql.database.azure.com"
    woord = request.form.get('woord')
    tekst = ""
    wachtwoord = request.form.get('ww')
    gebruiker = request.form.get('gebruiker')
    if woord == None:
        woord = ""
    if wachtwoord == None:
        wachtwoord = ""
    print(wachtwoord)
    tekst = """<link rel="stylesheet" href="https://unpkg.com/picnic"><form method="post">
             Gebruiker : <input type="text" name="gebruiker"></input><br>
             Wachtwoord: <input type="password" name="ww" value={}></input><br><hr>
             Zoekwoord : <input type="text" name="woord" value="">
             <input type="submit" value="Submit">
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
                                       user=gebruiker + "@" + hostname,
                                       passwd=wachtwoord)
        cursor = conn.cursor()
        cursor.execute("use dummy")
        cursor.execute(query)

        for bericht in cursor:
            tekst += "<div class=\"flex two three-600 six-1200 demo\">"
            tekst += "<div><span>" + bericht[0] + "</span></div>"
            tekst += "<div><span>" + str(bericht[2]) + ' ' + bericht[3] + "</span></div>"
            tekst += "<div><span>"+ bericht[1] + "</span></div></div>"
        cursor.close()
        conn.close()
    except Exception as e:
        tekst += "Er gaat iets mis met de database connectie<br>" + str(e)
    return tekst


@app.route("/bio")
def convert():
    tekst = """<form method="get">DNA sequentie:
        <input type="text" name="dna">
        <input type="submit" value="Submit">
        </form><hr>Eiwit sequentie:"""
    dna = request.args.get('dna')

    if dna == None:
        dna = ""
    dnaseq = Seq(dna)
    eiwit = dnaseq.translate()
    print(eiwit)
    return tekst + str(eiwit)
