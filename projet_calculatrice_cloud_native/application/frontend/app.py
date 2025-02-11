import os
from flask import Flask, render_template

app = Flask(__name__)

# Récupérer la variable d'environnement
backend_url = os.environ.get('BACKEND_HOST', 'http://localhost:5000')

@app.route('/')
def index():
    # Passer la variable d'environnement à ton template HTML
    return render_template('home.html', backend_url=backend_url)

@app.route('/calculator')
def calculator():
    # Passer la variable d'environnement à ton template HTML
    return render_template('calculator.html', backend_url=backend_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
