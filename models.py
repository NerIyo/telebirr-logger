from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class PaymentLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(15))
    amount = db.Column(db.Float)
    transaction_id = db.Column(db.String(50), unique=True)
    status = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime)

    def to_dict(self):
        return {
            "id": self.id,
            "phone_number": self.phone_number,
            "amount": self.amount,
            "transaction_id": self.transaction_id,
            "status": self.status,
            "timestamp": self.timestamp.isoformat()
        }
