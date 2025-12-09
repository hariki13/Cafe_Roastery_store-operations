"""Color measurement model for roast level analysis."""
from datetime import datetime
from app import db


class ColorMeasurement(db.Model):
    """Color measurement model for tracking roast levels."""
    
    __tablename__ = 'color_measurements'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Batch reference
    batch_id = db.Column(db.Integer, db.ForeignKey('roast_batches.id'), nullable=False)
    
    # Measurement details
    measurement_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Color values (multiple scale support)
    agtron_value = db.Column(db.Float)  # Agtron scale (higher = lighter)
    colortrack_value = db.Column(db.Float)  # Colortrack scale
    
    # Roast level classification
    roast_level = db.Column(db.String(32))  # light, medium-light, medium, medium-dark, dark
    
    # Measurement method
    measurement_method = db.Column(db.String(32))  # manual, hardware, visual
    
    # Sample information
    sample_type = db.Column(db.String(32))  # whole_bean, ground
    sample_location = db.Column(db.String(64))  # Location in batch where sample was taken
    
    # Notes
    notes = db.Column(db.Text)
    
    # User tracking
    measured_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    measurer = db.relationship('User', backref='color_measurements')
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_roast_level_from_agtron(self):
        """Classify roast level based on Agtron value.
        
        Agtron scale (approximate):
        - 95+: Very Light
        - 85-94: Light
        - 75-84: Medium-Light
        - 65-74: Medium
        - 55-64: Medium-Dark
        - 45-54: Dark
        - Below 45: Very Dark
        """
        if not self.agtron_value:
            return None
        
        if self.agtron_value >= 95:
            return 'very-light'
        elif self.agtron_value >= 85:
            return 'light'
        elif self.agtron_value >= 75:
            return 'medium-light'
        elif self.agtron_value >= 65:
            return 'medium'
        elif self.agtron_value >= 55:
            return 'medium-dark'
        elif self.agtron_value >= 45:
            return 'dark'
        else:
            return 'very-dark'
    
    def __repr__(self):
        return f'<ColorMeasurement Batch:{self.batch_id} - {self.roast_level}>'
