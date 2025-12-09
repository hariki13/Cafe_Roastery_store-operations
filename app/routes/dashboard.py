"""Dashboard routes."""
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app import db
from app.models import RoastBatch, GreenBeanInventory, RoastedCoffeeInventory, CuppingSession, FinancialRecord
from sqlalchemy import func, desc
from datetime import datetime, timedelta

bp = Blueprint('dashboard', __name__)


@bp.route('/')
@bp.route('/dashboard')
@login_required
def index():
    """Main dashboard view."""
    # Get statistics for widgets
    total_batches = RoastBatch.query.count()
    total_green_beans = GreenBeanInventory.query.filter_by(is_active=True).count()
    total_roasted = RoastedCoffeeInventory.query.filter_by(is_active=True).count()
    
    # Recent batches
    recent_batches = RoastBatch.query.order_by(desc(RoastBatch.roast_date)).limit(5).all()
    
    # Low stock alerts
    low_stock_items = GreenBeanInventory.query.filter_by(is_low_stock=True, is_active=True).all()
    
    # Recent cupping scores
    recent_cuppings = CuppingSession.query.order_by(desc(CuppingSession.session_date)).limit(5).all()
    
    # Financial summary for current month
    today = datetime.utcnow()
    month_start = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    monthly_revenue = db.session.query(func.sum(FinancialRecord.amount)).filter(
        FinancialRecord.record_type == 'revenue',
        FinancialRecord.record_date >= month_start
    ).scalar() or 0
    
    monthly_expenses = db.session.query(func.sum(FinancialRecord.amount)).filter(
        FinancialRecord.record_type == 'expense',
        FinancialRecord.record_date >= month_start
    ).scalar() or 0
    
    # Upcoming roasts (scheduled batches without end_time)
    upcoming_roasts = RoastBatch.query.filter(
        RoastBatch.end_time.is_(None),
        RoastBatch.roast_date >= today
    ).order_by(RoastBatch.roast_date).limit(5).all()
    
    return render_template('dashboard/index.html',
                         total_batches=total_batches,
                         total_green_beans=total_green_beans,
                         total_roasted=total_roasted,
                         recent_batches=recent_batches,
                         low_stock_items=low_stock_items,
                         recent_cuppings=recent_cuppings,
                         monthly_revenue=monthly_revenue,
                         monthly_expenses=monthly_expenses,
                         upcoming_roasts=upcoming_roasts)
