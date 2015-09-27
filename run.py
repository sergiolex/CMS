from app import app
from flask import Flask, render_template, redirect, request
app = Flask(__name__, template_folder='app/templates')



@app.route("/")
def hello():
    return render_template('HolaMundo.html')

@app.route("/Nombre", methods=['post'])
def HolaNombre():
    text = request.form['name']
    p_text = text.upper()
    return render_template('HolaNombre.html',name=p_text)
    

app.run(host='0.0.0.0', port=8080, debug=True)
