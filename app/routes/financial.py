"""Financial management routes."""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import FinancialRecord, RoastBatch
from sqlalchemy import func
from datetime import datetime, timedelta

bp = Blueprint('financial', __name__, url_prefix='/financial')


@bp.route('/')
@login_required
def index():
    """Financial overview and reports."""
    # Get date range from request
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Default to current month
    if not start_date:
        start_date = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0)
    else:
        start_date = datetime.fromisoformat(start_date)
    
    if not end_date:
        end_date = datetime.utcnow()
    else:
        end_date = datetime.fromisoformat(end_date)
    
    # Query financial records
    records = FinancialRecord.query.filter(
        FinancialRecord.record_date >= start_date,
        FinancialRecord.record_date <= end_date
    ).order_by(FinancialRecord.record_date.desc()).all()
    
    # Calculate totals
    total_revenue = sum(r.amount for r in records if r.record_type == 'revenue')
    total_expenses = sum(r.amount for r in records if r.record_type == 'expense')
    total_cogs = sum(r.amount for r in records if r.record_type == 'cogs')
    
    profit = total_revenue - total_expenses - total_cogs
    
    return render_template('financial/index.html',
                         records=records,
                         total_revenue=total_revenue,
                         total_expenses=total_expenses,
                         total_cogs=total_cogs,
                         profit=profit,
                         start_date=start_date,
                         end_date=end_date)


@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_record():
    """Create new financial record."""
    if request.method == 'POST':
        record = FinancialRecord(
            record_type=request.form.get('record_type'),
            category=request.form.get('category'),
            amount=float(request.form.get('amount', 0)),
            description=request.form.get('description'),
            created_by=current_user.id
        )
        db.session.add(record)
        db.session.commit()
        flash('Financial record created!', 'success')
        return redirect(url_for('financial.index'))
    
    return render_template('financial/form.html')
