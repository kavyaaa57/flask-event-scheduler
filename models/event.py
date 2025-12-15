from extensions import db
class Event(db.Model):
    __tablename__ = 'events'
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String, nullable=False)
    event_type=db.Column(db.String, nullable=False)
    start_time=db.Column(db.DateTime, nullable=False)
    end_time=db.Column(db.DateTime, nullable=False)
    description=db.Column(db.Text)