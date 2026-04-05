import uuid
from datetime import date
from extensions import db

class Record(db.Model):
    __tablename__ = "records"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(10), nullable=False, default=lambda: str(date.today()))
    notes = db.Column(db.String(500), default="")
    deleted = db.Column(db.Boolean, default=False)

    TYPES = ["income", "expense"]

    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "type": self.type,
            "category": self.category,
            "date": self.date,
            "notes": self.notes,
        }
