from flask import Flask, render_template, request
import dao
import json

app = Flask(__name__)

@app.route('/courts')
def courts():
    civil_freq= dao.get_court_civil_freq()
    criminal_freq= dao.get_court_criminal_freq()
    print({'civil_freq':civil_freq, 'criminal_freq':criminal_freq})
    return render_template('menu.html', freq={'civil_freq':civil_freq, 'criminal_freq':criminal_freq})

@app.route('/court_precedent')
def court_precedent():
    name= request.args.get('name','')
    civil_pre= dao.get_court_civil_precedents(name)
    criminal_pre= dao.get_court_criminal_precedents(name)
    for idx in range(len(civil_pre)):
        civil_pre[idx]['판결날짜']= str(civil_pre[idx]['판결날짜'])
    for idx in range(len(criminal_pre)):
        criminal_pre[idx]['판결날짜']= str(civil_pre[idx]['판결날짜'])
    print(civil_pre)
    return json.dumps({'civil':criminal_pre,'criminal':criminal_pre})

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('menu.html', name=name)

if __name__ == '__main__':
    app.run()


