"""Inventory management models."""
from datetime import datetime
from app import db


class GreenBeanInventory(db.Model):
    """Green bean inventory model."""
    
    __tablename__ = 'green_bean_inventory'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Bean information
    name = db.Column(db.String(128), nullable=False)
    variety = db.Column(db.String(64))
    origin = db.Column(db.String(128), index=True)
    region = db.Column(db.String(128))
    processing_method = db.Column(db.String(64))
    
    # Stock information
    current_stock = db.Column(db.Float, default=0.0)  # Current stock in kg
    unit_cost = db.Column(db.Float, nullable=False)  # Cost per kg
    
    # Supplier information
    supplier_name = db.Column(db.String(128))
    supplier_contact = db.Column(db.String(128))
    
    # Quality and tracking
    arrival_date = db.Column(db.DateTime)
    harvest_date = db.Column(db.DateTime)
    days_since_arrival = db.Column(db.Integer)
    
    # Alerts
    low_stock_threshold = db.Column(db.Float, default=10.0)  # Alert when below this
    is_low_stock = db.Column(db.Boolean, default=False)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    transactions = db.relationship('InventoryTransaction', 
                                   foreign_keys='InventoryTransaction.green_bean_id',
                                   backref='green_bean', lazy='dynamic')
    
    def update_days_since_arrival(self):
        """Update days since arrival."""
        if self.arrival_date:
            delta = datetime.utcnow() - self.arrival_date
            self.days_since_arrival = delta.days
    
    def check_low_stock(self):
        """Check if stock is low."""
        self.is_low_stock = self.current_stock <= self.low_stock_threshold
    
    def __repr__(self):
        return f'<GreenBean {self.name} - {self.origin}>'


class RoastedCoffeeInventory(db.Model):
    """Roasted coffee inventory model."""
    
    __tablename__ = 'roasted_coffee_inventory'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Product information
    sku = db.Column(db.String(64), unique=True, nullable=False, index=True)
    product_name = db.Column(db.String(128), nullable=False)
    roast_level = db.Column(db.String(32))
    
    # Stock information
    current_stock = db.Column(db.Float, default=0.0)  # Current stock in kg
    unit_cost = db.Column(db.Float)  # Cost per kg (COGM)
    selling_price = db.Column(db.Float)  # Selling price per kg
    
    # Tracking
    roast_date = db.Column(db.DateTime, index=True)
    shelf_life_days = db.Column(db.Integer, default=90)  # Default 90 days
    expiry_date = db.Column(db.DateTime)
    days_until_expiry = db.Column(db.Integer)
    
    # Profile reference
    profile_id = db.Column(db.Integer, db.ForeignKey('roast_profiles.id'))
    profile = db.relationship('RoastProfile', backref='roasted_inventory')
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    transactions = db.relationship('InventoryTransaction',
                                   foreign_keys='InventoryTransaction.roasted_coffee_id',
                                   backref='roasted_coffee', lazy='dynamic')
    
    def calculate_expiry(self):
        """Calculate expiry date."""
        if self.roast_date and self.shelf_life_days:
            from datetime import timedelta
            self.expiry_date = self.roast_date + timedelta(days=self.shelf_life_days)
            delta = self.expiry_date - datetime.utcnow()
            self.days_until_expiry = max(0, delta.days)
    
    def calculate_margin(self):
        """Calculate profit margin percentage."""
        if self.unit_cost and self.selling_price:
            return ((self.selling_price - self.unit_cost) / self.selling_price) * 100
        return 0
    
    def __repr__(self):
        return f'<RoastedCoffee {self.sku} - {self.product_name}>'


class InventoryTransaction(db.Model):
    """Inventory transaction model for tracking all inventory movements."""
    
    __tablename__ = 'inventory_transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Transaction type
    transaction_type = db.Column(db.String(32), nullable=False)  # purchase, roast, sale, waste, adjustment
    
    # Item references (one will be null depending on transaction type)
    green_bean_id = db.Column(db.Integer, db.ForeignKey('green_bean_inventory.id'))
    roasted_coffee_id = db.Column(db.Integer, db.ForeignKey('roasted_coffee_inventory.id'))
    
    # Transaction details
    quantity = db.Column(db.Float, nullable=False)  # Quantity in kg (positive or negative)
    unit_cost = db.Column(db.Float)
    total_cost = db.Column(db.Float)
    
    # Reference information
    reference_id = db.Column(db.String(64))  # Order ID, Batch ID, etc.
    notes = db.Column(db.Text)
    
    # Metadata
    transaction_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    creator = db.relationship('User', backref='created_inventory_transactions')
    
    def __repr__(self):
        return f'<Transaction {self.transaction_type} - {self.quantity}kg>'
