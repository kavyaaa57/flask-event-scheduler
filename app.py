from flask import Flask, render_template
from flask import request, redirect, url_for
from datetime import datetime
from models.event import Event
from models.resource import Resource
from extensions import db

app=Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)
@app.route('/')
def hello():
    return render_template('index.html')
@app.route('/events')
def event_list():
    events=Event.query.all()
    return render_template('events/list.html', events=events)
@app.route('/events/add', methods=['GET','POST'])
def add_event():
    if request.method=='POST':
        event=Event(
            title=request.form['title'],
            event_type=request.form['event_type'],
            start_time=datetime.fromisoformat(request.form['start_time']),
            end_time=datetime.fromisoformat(request.form['end_time']),
            description=request.form['description']
        )
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('event_list'))
        
    return render_template('events/add.html')

@app.route('/resources')
def resource_list():
    resources=Resource.query.all()
    return render_template('resources/list.html', resources=resources)

@app.route('/resources/add', methods=['GET', 'POST'])
def add_resources():
    if request.method=='POST':
        resource=Resource(
            resource_name=request.form['resource_name'],
            resource_type=request.form['resource_type'],
            resource_qty=request.form['resource_qty']
        )
        db.session.add(resource)
        db.session.commit()
        return redirect(url_for('resource_list'))

    return render_template('resources/add.html')
if __name__=='__main__':
    app.run(debug=True)