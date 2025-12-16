from flask import Flask, render_template
from flask import request, redirect, url_for
from datetime import datetime
from models.event import Event
from models.resource import Resource
from models.allocation import Allocation
from extensions import db
from collections import defaultdict

app=Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)
@app.route('/')
def home():
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

@app.route('/allocations')
def allocation_list():
    allocations = Allocation.query.all()

    grouped = defaultdict(list)
    for alloc in allocations:
        grouped[alloc.event].append(alloc)

    return render_template(
        'allocations/list.html',
        grouped_allocations=grouped
    )

@app.route('/allocations/add', methods=['GET', 'POST'])
def add_allocation():
    if request.method=='POST':
        event_id=int(request.form['event_id'])
        resource_id=int(request.form['resource_id'])
        qty=int(request.form['qty_allocated'])
        event=Event.query.get(event_id)
        resource=Resource.query.get(resource_id)
        new_start=event.start_time
        new_end=event.end_time
        conflict=(db.session.query(Allocation).join(Event).filter(
            Allocation.resource_id==resource_id, Event.start_time<new_end, Event.end_time>new_start).first()
        )
        if conflict:
            return "Resource already allocated for this time period"
        allocated=(db.session.query(
            db.func.sum(Allocation.qty_allocated)).join(Event).filter(Allocation.resource_id==resource_id, Event.start_time<new_end, Event.end_time>new_start).scalar() or 0)
        available=resource.resource_qty-allocated
        if qty>available:
            return "Not enough resource available"
        allocation=Allocation(event_id=event_id, resource_id=resource_id, qty_allocated=qty)
        db.session.add(allocation)
        db.session.commit()
        return redirect(url_for('allocation_list'))
    events=Event.query.all()
    resources=Resource.query.all()

    return render_template('allocations/add.html', events=events, resources=resources)

@app.route('/conflicts')
def conflict_list():
    conflicts=[]
    allocations=(db.session.query(Allocation).join(Event).join(Resource).all())
    for i in range(len(allocations)):
        for j in range(i+1, len(allocations)):
            a1=allocations[i]
            a2=allocations[j]
            if a1.resource_id==a2.resource_id and a1.event_id!=a2.event_id:
                e1 = a1.event
                e2 = a2.event
                if e1.start_time<e2.end_time and e1.end_time>e2.start_time:
                    conflicts.append({
                        "resource":a1.resource.resource_name,
                        "event1":e1.title,
                        "event2":e2.title,
                        "time1":f"{e1.start_time}-{e1.end_time}",
                        "time2":f"{e2.start_time}-{e2.end_time}",
                    })

    return render_template("conflicts/list.html", conflicts=conflicts)

@app.route('/reports/utilisation_list', methods=['GET','POST'])
def resource_utilisation():
    report=[]
    start_date=None
    end_date=None
    if request.method=='POST':
        start_date=datetime.fromisoformat(request.form['start_date'])
        end_date=datetime.fromisoformat(request.form['end_date'])
        resources=Resource.query.all()
        for resource in resources:
            total_hours=0
            upcoming=0
            allocations=(db.session.query(Allocation).join(Event).filter(
                Allocation.resource_id==resource.id,Event.start_time>=start_date,Event.end_time<=end_date).all())
            for alloc in allocations:
                event=alloc.event
                duration=(event.end_time-event.start_time).total_seconds()/3600
                total_hours+=duration*alloc.qty_allocated
                upcoming=(db.session.query(Allocation).join(Event).filter(
                    Allocation.resource_id==resource.id,Event.start_time>=datetime.now()).count())

            report.append({"resource":resource.resource_name,"total_hours":round(total_hours, 2),"upcoming":upcoming})

    return render_template(
        'reports/utilisation_list.html',report=report,start_date=start_date,end_date=end_date)


if __name__=='__main__':
    app.run(debug=True)