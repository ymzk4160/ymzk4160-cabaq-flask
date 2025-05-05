from datetime import datetime
from app.extensions import db

class Payment(db.Model):
    __tablename__ = 'payments'
    
    # 基本情報
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    plan_type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(3), default='JPY')
    
    # Stripe連携情報
    stripe_customer_id = db.Column(db.String(255))
    stripe_subscription_id = db.Column(db.String(255))
    stripe_payment_method_id = db.Column(db.String(255))
    stripe_invoice_id = db.Column(db.String(255))
    
    # 支払い状態
    status = db.Column(db.String(50), default='active')
    is_active = db.Column(db.Boolean, default=True)
    payment_method = db.Column(db.String(50))
    
    # 日時情報
    start_date = db.Column(db.DateTime)
    trial_end_date = db.Column(db.DateTime)
    next_billing_date = db.Column(db.DateTime)
    cancel_at = db.Column(db.DateTime)
    canceled_at = db.Column(db.DateTime)
    last_payment_at = db.Column(db.DateTime)
    
    # 通知/管理情報
    trial_reminder_sent = db.Column(db.Boolean, default=False)
    cancel_reason = db.Column(db.Text)
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    # リレーション設定
    user = db.relationship('User', backref=db.backref('payments', lazy=True)) 
