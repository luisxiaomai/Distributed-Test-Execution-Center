from . import db
from datetime import datetime

class Record(db.Model):
    __tableName_ = "Record"
    id = db.Column(db.Integer, primary_key=True)
    test_cases = db.Column(db.String(64))
    owner= db.Column(db.String(64), default="test")
    start_time = db.Column(db.String(64))
    end_time = db.Column(db.String(64))
    status = db.Column(db.String(64))
    log_path = db.Column(db.String(64))
    message = db.Column(db.String())
    task_id = db.Column(db.String(64))

    
    def to_json(self):
        return {
            'id':self.id,
            'test_cases':self.test_cases,
            'owner':self.owner,
            'start_time':self.start_time,
            'end_time':self.end_time,
            'status':self.status,
            'log_path':self.log_path,
            'task_id':self.task_id,
            'message':self.message
        }
