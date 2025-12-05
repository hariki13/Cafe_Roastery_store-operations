"""Batch comparison routes."""
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required
from app import db
from app.models import RoastBatch, CuppingSession, ColorMeasurement

bp = Blueprint('comparison', __name__, url_prefix='/comparison')


@bp.route('/')
@login_required
def index():
    """Batch comparison tool."""
    batches = RoastBatch.query.order_by(RoastBatch.roast_date.desc()).limit(50).all()
    return render_template('comparison/index.html', batches=batches)


@bp.route('/compare', methods=['POST'])
@login_required
def compare():
    """Compare selected batches."""
    batch_ids = request.form.getlist('batch_ids[]')
    
    if not batch_ids or len(batch_ids) < 2:
        flash('Please select at least 2 batches to compare', 'warning')
        return redirect(url_for('comparison.index'))
    
    # Get batch data
    batches = []
    for batch_id in batch_ids:
        batch = RoastBatch.query.get(int(batch_id))
        if batch:
            # Get associated data
            cupping = batch.cupping_sessions.first()
            color = batch.color_measurements.first()
            
            batches.append({
                'batch': batch,
                'cupping': cupping,
                'color': color
            })
    
    return render_template('comparison/compare.html', batches=batches)


@bp.route('/api/batch/<int:id>')
@login_required
def batch_data(id):
    """Get batch data as JSON for API access."""
    batch = RoastBatch.query.get_or_404(id)
    cupping = batch.cupping_sessions.first()
    color = batch.color_measurements.first()
    
    return jsonify({
        'batch': {
            'id': batch.id,
            'batch_id': batch.batch_id,
            'roast_date': batch.roast_date.isoformat() if batch.roast_date else None,
            'green_weight': batch.green_weight,
            'roasted_weight': batch.roasted_weight,
            'weight_loss_pct': batch.weight_loss_pct,
            'roast_level': batch.roast_level,
            'total_cost': batch.total_cost
        },
        'cupping': {
            'final_score': cupping.final_score if cupping else None,
            'tasting_notes': cupping.tasting_notes if cupping else None
        } if cupping else None,
        'color': {
            'agtron_value': color.agtron_value if color else None,
            'roast_level': color.roast_level if color else None
        } if color else None
    })
