from app import db
from datetime import datetime, time
from sqlalchemy import Time

class Operation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    entry_time = db.Column(Time, nullable=False)
    exit_time = db.Column(Time, nullable=False)
    stop_loss = db.Column(db.Float, nullable=False)
    stop_profit = db.Column(db.Float, nullable=True)
    direction = db.Column(db.String(5), nullable=False)
    broker = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    entry_price = db.Column(db.Float)
    exit_price = db.Column(db.Float)
    enviada = db.Column(db.Boolean, default=False)

    @property
    def ganancia(self):
        if self.entry_price is not None and self.exit_price is not None:
            if self.direction == "long":
                return round((self.exit_price - self.entry_price) * self.amount, 2)
            elif self.direction == "short":
                return round((self.entry_price - self.exit_price) * self.amount, 2)
        return None