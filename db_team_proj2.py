
from flask import Flask, render_template
import dao
import json

app = Flask(__name__)

@app.route('/courts')
def courts():
    civil_freq= dao.get_court_civil_freq()
    criminal_freq= dao.get_court_criminal_freq()
    print({'civil_freq':civil_freq, 'criminal_freq':criminal_freq})
    return render_template('menu.html', freq={'civil_freq':civil_freq, 'criminal_freq':criminal_freq})

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('menu.html', name=name)

if __name__ == '__main__':
    app.run()


