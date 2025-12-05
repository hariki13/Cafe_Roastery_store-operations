"""Roast profile and batch models."""
from datetime import datetime
from app import db


class RoastProfile(db.Model):
    """Roast profile model for storing roast parameters."""
    
    __tablename__ = 'roast_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, index=True)
    description = db.Column(db.Text)
    
    # Bean information
    bean_type = db.Column(db.String(64))
    origin = db.Column(db.String(128))
    processing_method = db.Column(db.String(64))
    
    # Target parameters
    target_temp = db.Column(db.Float)  # Target temperature
    target_time = db.Column(db.Integer)  # Target time in seconds
    target_roast_level = db.Column(db.String(32))  # light, medium, dark
    development_time = db.Column(db.Integer)  # Development time in seconds
    
    # Temperature curve (stored as JSON string)
    temp_curve = db.Column(db.Text)  # JSON array of temp/time points
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    batches = db.relationship('RoastBatch', backref='profile', lazy='dynamic')
    
    def __repr__(self):
        return f'<RoastProfile {self.name}>'


class RoastBatch(db.Model):
    """Roast batch model for individual roast sessions."""
    
    __tablename__ = 'roast_batches'
    
    id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.String(64), unique=True, nullable=False, index=True)
    
    # Profile and operator
    profile_id = db.Column(db.Integer, db.ForeignKey('roast_profiles.id'))
    operator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Timing
    roast_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    duration = db.Column(db.Integer)  # Duration in seconds
    
    # Weight tracking
    green_weight = db.Column(db.Float, nullable=False)  # Input weight in kg
    roasted_weight = db.Column(db.Float, nullable=False)  # Output weight in kg
    weight_loss_pct = db.Column(db.Float)  # Calculated weight loss percentage
    
    # Roast characteristics
    roast_level = db.Column(db.String(32))  # light, medium, dark
    development_time = db.Column(db.Integer)  # Actual development time
    first_crack_time = db.Column(db.Integer)  # Time to first crack in seconds
    end_temp = db.Column(db.Float)  # Final temperature
    
    # Notes and observations
    notes = db.Column(db.Text)
    
    # Quality and cost
    quality_score = db.Column(db.Float)  # Overall quality score
    green_bean_cost = db.Column(db.Float)  # Cost of green beans used
    labor_cost = db.Column(db.Float)  # Labor cost for this batch
    energy_cost = db.Column(db.Float)  # Energy cost for this batch
    total_cost = db.Column(db.Float)  # Total cost (COGM)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    cupping_sessions = db.relationship('CuppingSession', backref='batch', lazy='dynamic')
    color_measurements = db.relationship('ColorMeasurement', backref='batch', lazy='dynamic')
    
    def calculate_weight_loss(self):
        """Calculate weight loss percentage."""
        if self.green_weight and self.roasted_weight:
            self.weight_loss_pct = ((self.green_weight - self.roasted_weight) / self.green_weight) * 100
    
    def calculate_total_cost(self):
        """Calculate total cost (COGM)."""
        costs = [
            self.green_bean_cost or 0,
            self.labor_cost or 0,
            self.energy_cost or 0
        ]
        self.total_cost = sum(costs)
    
    def __repr__(self):
        return f'<RoastBatch {self.batch_id}>'
