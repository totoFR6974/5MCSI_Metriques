from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)    

@app.route("/contact/")
def contact():
    return render_template("contact.html")
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')
  
if __name__ == "__main__":
  app.run(debug=True)

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)



@app.route("/graphique/")
def monhistogramme():
    return render_template("histogramme.html")

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")


from flask import Flask, render_template, jsonify
import urllib.request, json
from datetime import datetime

# ... (votre code précédent) ...

@app.route('/commits/')
def commits():
    return render_template("commits.html")

@app.route('/commits-data/')
def commits_data():
    # URL de l'API GitHub pour votre repository
    url = 'https://api.github.com/repos/totoFR6974/5MCSI_Metriques/commits'
    
    # GitHub demande un User-Agent pour accepter la requête
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    with urllib.request.urlopen(req) as response:
        raw_content = response.read()
        json_content = json.loads(raw_content.decode('utf-8'))
    
    # On crée une liste de 60 compteurs (un pour chaque minute de 0 à 59)
    # Initialisée à 0 : [0, 0, 0, ..., 0]
    minute_counts = [0] * 60
    
    for commit in json_content:
        # On récupère la date du commit : [commit][commit][author][date]
        date_string = commit['commit']['author']['date']
        
        # On transforme la chaîne "2024-02-11T11:57:27Z" en objet datetime
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        
        # On extrait la minute
        minute = date_object.minute
        
        # On incrémente le compteur pour cette minute précise
        minute_counts[minute] += 1
    
    # On prépare les données pour Google Charts
    # Format attendu : [ ["Minute", "Nombre de commits"], ["0", 2], ["1", 0], ... ]
    results = []
    for i in range(60):
        results.append({'minute': i, 'count': minute_counts[i]})
        
    return jsonify(results=results)
