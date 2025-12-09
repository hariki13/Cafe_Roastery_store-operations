"""Cupping session and scoring models."""
from datetime import datetime
from app import db


class CuppingSession(db.Model):
    """Cupping session model following SCA protocols."""
    
    __tablename__ = 'cupping_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Session information
    session_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    evaluator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Batch reference
    batch_id = db.Column(db.Integer, db.ForeignKey('roast_batches.id'))
    
    # SCA Scoring (out of 10 each, following SCA protocol)
    fragrance_aroma = db.Column(db.Float)  # Dry/wet aroma
    flavor = db.Column(db.Float)
    aftertaste = db.Column(db.Float)
    acidity = db.Column(db.Float)
    body = db.Column(db.Float)
    balance = db.Column(db.Float)
    sweetness = db.Column(db.Float)  # Usually 10 for specialty
    clean_cup = db.Column(db.Float)  # Usually 10 for specialty
    uniformity = db.Column(db.Float)  # Usually 10 for specialty
    overall = db.Column(db.Float)  # Overall impression
    
    # Total score (sum of all attributes)
    total_score = db.Column(db.Float)
    
    # Defects
    defects = db.Column(db.Integer, default=0)  # Number of defects
    defect_intensity = db.Column(db.Integer, default=0)  # 2 or 4 points per defect
    defects_deduction = db.Column(db.Float, default=0.0)
    
    # Final score (total - defects)
    final_score = db.Column(db.Float)
    
    # Tasting notes
    tasting_notes = db.Column(db.Text)
    defect_notes = db.Column(db.Text)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def calculate_scores(self):
        """Calculate total and final scores."""
        # Sum all scoring attributes
        scores = [
            self.fragrance_aroma or 0,
            self.flavor or 0,
            self.aftertaste or 0,
            self.acidity or 0,
            self.body or 0,
            self.balance or 0,
            self.sweetness or 0,
            self.clean_cup or 0,
            self.uniformity or 0,
            self.overall or 0
        ]
        self.total_score = sum(scores)
        
        # Calculate defects deduction
        self.defects_deduction = self.defects * self.defect_intensity
        
        # Calculate final score
        self.final_score = self.total_score - self.defects_deduction
    
    def get_grade(self):
        """Get SCA grade based on final score."""
        if not self.final_score:
            return 'Not Scored'
        
        if self.final_score >= 90:
            return 'Outstanding'
        elif self.final_score >= 85:
            return 'Excellent'
        elif self.final_score >= 80:
            return 'Very Good'
        elif self.final_score >= 75:
            return 'Good'
        elif self.final_score >= 70:
            return 'Fair'
        else:
            return 'Below Specialty'
    
    def __repr__(self):
        return f'<CuppingSession {self.id} - Score: {self.final_score}>'


class CuppingScore(db.Model):
    """Historical cupping scores for trending and analysis."""
    
    __tablename__ = 'cupping_scores'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('cupping_sessions.id'))
    session = db.relationship('CuppingSession', backref='score_history')
    
    # Simplified score tracking for charts
    score_date = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    final_score = db.Column(db.Float, nullable=False)
    batch_id = db.Column(db.Integer, db.ForeignKey('roast_batches.id'))
    
    def __repr__(self):
        return f'<CuppingScore {self.final_score}>'
