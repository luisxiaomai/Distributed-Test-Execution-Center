from . import db
from datetime import datetime

class Record(db.Model):
    __tableName_ = "Record"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    owner= db.Column(db.String(64))
    start_time = db.Column(db.String(64))
    end_time = db.Column(db.String(64))
    status = db.Column(db.String(64))
    log_path = db.Column(db.String(64))
    task_id = db.Column(db.String(64))
    def __repr__(self):
        return "<Record %r>"%self.name
    
    def to_json(self):
        return {
            'id':self.id,
            'name':self.name,
            'owner':self.owner,
            'start_time':self.start_time,
            'end_time':self.end_time,
            'status':self.status,
            'log_path':self.log_path,
            'task_id':self.task_id,
        }
