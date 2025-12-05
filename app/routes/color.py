"""Color analyzer routes."""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import ColorMeasurement, RoastBatch

bp = Blueprint('color', __name__, url_prefix='/color')


@bp.route('/')
@login_required
def index():
    """List color measurements."""
    page = request.args.get('page', 1, type=int)
    measurements = ColorMeasurement.query.order_by(
        ColorMeasurement.measurement_date.desc()
    ).paginate(page=page, per_page=20, error_out=False)
    return render_template('color/index.html', measurements=measurements)


@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_measurement():
    """Create new color measurement."""
    if request.method == 'POST':
        measurement = ColorMeasurement(
            batch_id=int(request.form.get('batch_id')),
            agtron_value=float(request.form.get('agtron_value', 0)) if request.form.get('agtron_value') else None,
            colortrack_value=float(request.form.get('colortrack_value', 0)) if request.form.get('colortrack_value') else None,
            measurement_method=request.form.get('measurement_method', 'manual'),
            sample_type=request.form.get('sample_type', 'whole_bean'),
            notes=request.form.get('notes'),
            measured_by=current_user.id
        )
        
        # Auto-classify roast level from Agtron value
        if measurement.agtron_value:
            measurement.roast_level = measurement.get_roast_level_from_agtron()
        else:
            measurement.roast_level = request.form.get('roast_level')
        
        db.session.add(measurement)
        db.session.commit()
        flash('Color measurement added!', 'success')
        return redirect(url_for('color.index'))
    
    batches = RoastBatch.query.order_by(RoastBatch.roast_date.desc()).limit(50).all()
    return render_template('color/form.html', batches=batches)
