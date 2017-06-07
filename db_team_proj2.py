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
    name= request.args.get('name', '')
    civil_pre= dao.get_court_civil_precedents(name)
    criminal_pre= dao.get_court_criminal_precedents(name)
    for idx in range(len(civil_pre)):
        civil_pre[idx]['판결날짜']= str(civil_pre[idx]['판결날짜'])
    for idx in range(len(criminal_pre)):
        criminal_pre[idx]['판결날짜']= str(criminal_pre[idx]['판결날짜'])
    return json.dumps({'civil':civil_pre, 'criminal':criminal_pre})

@app.route('/precedents')
def civil_precedents():
    kind= request.args.get('kind')
    reject= request.args.get('reject')

    if kind== 'civil':
        dao.get_criminal_precedents()
        pass
    else:
        dao.get_civil_precedents()
        pass
    return

@app.route('/criminal_statics')
def criminal_statics():
    return render_template('criminal_statics.html')

@app.route('/accused_search')
def accused_search():

    return render_template('accused_search.html')

@app.route('/get_top_accused')
def get_top_accused():
    return json.dumps(dao.get_top_accused())

@app.route('/get_accused_id')
def get_accused_id():
    accused_id = request.args.get('accused_id')
    return json.dumps(dao.get_accused_info(accused_id))

@app.route('/get_criminal_pie')
def get_criminal_pie():
    return json.dumps(dao.get_criminal_pie())

@app.route('/get_fine_pie')
def get_fine_pie():
    return json.dumps(dao.get_fine_pie())
@app.route('/get_servitude_pie')
def get_servitude_pie():
    return json.dumps(dao.get_servitude_pie())

@app.route('/precedent')
def precedent():
    return render_template('precedent.html', precedent= request.args.get('precedent'))

@app.route('/get_precedent')
def get_precedent():
    result={}
    precedent_id= request.args.get('precedent')
    civil_precedent= dao.get_civil_precedent(precedent_id)
    criminal_precedent= dao.get_criminal_precedent(precedent_id)

    if len(civil_precedent) != 0:
        result["type"] = "civil"
        result["precedent"] = civil_precedent
        result["evidence"] = dao.get_civil_evidence(precedent_id)
        #result["defendant"] = dao.get_civil_defendant(precedent_id)

    if len(criminal_precedent) != 0:
        result["type"] = "criminal"
        result["precedent"] = criminal_precedent
        result["evidence"] = dao.get_criminal_evidence(precedent_id)
        #result["defendant"] = dao.get_civil_defendant(precedent_id)

    return json.dumps(result)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('menu.html', name=name)

if __name__ == '__main__':
    app.run()


