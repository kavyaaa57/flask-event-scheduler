from extensions import db
class Resource(db.Model):
    __tablename__ = 'resources'
    id=db.Column(db.Integer, primary_key=True)
    resource_name=db.Column(db.String, nullable=True)
    resource_type=db.Column(db.String, nullable=True)
    resource_qty=db.Column(db.Integer, nullable=True)