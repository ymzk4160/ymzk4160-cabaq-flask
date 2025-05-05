from datetime import datetime
from app.extensions import db

class PaymentHistory(db.Model):
    __tablename__ = 'payment_histories'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.id'))
    transaction_type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(3), default='JPY')
    stripe_invoice_id = db.Column(db.String(255))
    stripe_payment_intent_id = db.Column(db.String(255))
    stripe_charge_id = db.Column(db.String(255))
    payment_method = db.Column(db.String(50))
    status = db.Column(db.String(50))
    error_message = db.Column(db.Text)
    receipt_url = db.Column(db.String(255))
    receipt_number = db.Column(db.String(50))
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # リレーション設定
    user = db.relationship('User', backref=db.backref('payment_histories', lazy=True))
    payment = db.relationship('Payment', backref=db.backref('histories', lazy=True))
