from extensions import db
class Allocation(db.Model):
    __tablename__ = 'allocations'
    id=db.Column(db.Integer, primary_key=True)
    event_id=db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    resource_id=db.Column(db.Integer, db.ForeignKey('resources.id'), nullable=False)
    qty_allocated=db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    event = db.relationship('Event', backref='allocations')
    resource = db.relationship('Resource', backref='allocations')