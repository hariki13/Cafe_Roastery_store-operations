"""Financial records model."""
from datetime import datetime
from app import db


class FinancialRecord(db.Model):
    """Financial record model for tracking costs and revenue."""
    
    __tablename__ = 'financial_records'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Record type
    record_type = db.Column(db.String(32), nullable=False, index=True)  # revenue, expense, cogs, cogm
    category = db.Column(db.String(64))  # green_beans, labor, energy, sales, packaging, overhead
    
    # Financial details
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    
    # References
    reference_type = db.Column(db.String(32))  # batch, purchase_order, sale_order
    reference_id = db.Column(db.String(64))
    batch_id = db.Column(db.Integer, db.ForeignKey('roast_batches.id'))
    batch = db.relationship('RoastBatch', backref='batch_financial_records')
    
    # Description
    description = db.Column(db.Text)
    notes = db.Column(db.Text)
    
    # Date tracking
    record_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # User tracking
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    creator = db.relationship('User', backref='user_financial_records')
    
    def __repr__(self):
        return f'<FinancialRecord {self.record_type} - {self.amount} {self.currency}>'
