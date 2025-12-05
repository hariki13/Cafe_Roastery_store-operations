"""Roast profiler routes."""
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import RoastProfile, RoastBatch, User
from datetime import datetime
import json

bp = Blueprint('roast', __name__, url_prefix='/roast')


@bp.route('/profiles')
@login_required
def profiles():
    """List all roast profiles."""
    page = request.args.get('page', 1, type=int)
    profiles = RoastProfile.query.filter_by(is_active=True).order_by(
        RoastProfile.created_at.desc()
    ).paginate(page=page, per_page=20, error_out=False)
    return render_template('roast/profiles.html', profiles=profiles)


@bp.route('/profiles/new', methods=['GET', 'POST'])
@login_required
def new_profile():
    """Create new roast profile."""
    if not current_user.is_roaster():
        flash('Only roasters can create profiles', 'warning')
        return redirect(url_for('roast.profiles'))
    
    if request.method == 'POST':
        try:
            profile = RoastProfile(
                name=request.form.get('name'),
                description=request.form.get('description'),
                bean_type=request.form.get('bean_type'),
                origin=request.form.get('origin'),
                processing_method=request.form.get('processing_method'),
                target_temp=float(request.form.get('target_temp') or 0),
                target_time=int(request.form.get('target_time') or 0),
                target_roast_level=request.form.get('target_roast_level'),
                development_time=int(request.form.get('development_time') or 0)
            )
            db.session.add(profile)
            db.session.commit()
            flash('Roast profile created successfully!', 'success')
            return redirect(url_for('roast.profile_detail', id=profile.id))
        except (ValueError, TypeError) as e:
            flash('Invalid input data. Please check your values.', 'danger')
            return redirect(url_for('roast.new_profile'))
    
    return render_template('roast/profile_form.html', profile=None)


@bp.route('/profiles/<int:id>')
@login_required
def profile_detail(id):
    """View roast profile details."""
    profile = RoastProfile.query.get_or_404(id)
    batches = profile.batches.order_by(RoastBatch.roast_date.desc()).limit(10).all()
    return render_template('roast/profile_detail.html', profile=profile, batches=batches)


@bp.route('/profiles/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_profile(id):
    """Edit roast profile."""
    if not current_user.is_roaster():
        flash('Only roasters can edit profiles', 'warning')
        return redirect(url_for('roast.profiles'))
    
    profile = RoastProfile.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            profile.name = request.form.get('name')
            profile.description = request.form.get('description')
            profile.bean_type = request.form.get('bean_type')
            profile.origin = request.form.get('origin')
            profile.processing_method = request.form.get('processing_method')
            profile.target_temp = float(request.form.get('target_temp') or 0)
            profile.target_time = int(request.form.get('target_time') or 0)
            profile.target_roast_level = request.form.get('target_roast_level')
            profile.development_time = int(request.form.get('development_time') or 0)
            profile.updated_at = datetime.utcnow()
            
            db.session.commit()
            flash('Roast profile updated successfully!', 'success')
            return redirect(url_for('roast.profile_detail', id=profile.id))
        except (ValueError, TypeError) as e:
            flash('Invalid input data. Please check your values.', 'danger')
            return redirect(url_for('roast.edit_profile', id=profile.id))
    
    return render_template('roast/profile_form.html', profile=profile)


@bp.route('/batches')
@login_required
def batches():
    """List all roast batches."""
    page = request.args.get('page', 1, type=int)
    batches = RoastBatch.query.order_by(
        RoastBatch.roast_date.desc()
    ).paginate(page=page, per_page=20, error_out=False)
    return render_template('roast/batches.html', batches=batches)


@bp.route('/batches/new', methods=['GET', 'POST'])
@login_required
def new_batch():
    """Create new roast batch."""
    if not current_user.is_roaster():
        flash('Only roasters can create batches', 'warning')
        return redirect(url_for('roast.batches'))
    
    if request.method == 'POST':
        batch = RoastBatch(
            batch_id=request.form.get('batch_id'),
            profile_id=int(request.form.get('profile_id')) if request.form.get('profile_id') else None,
            operator_id=current_user.id,
            green_weight=float(request.form.get('green_weight', 0)),
            roasted_weight=float(request.form.get('roasted_weight', 0)),
            roast_level=request.form.get('roast_level'),
            notes=request.form.get('notes')
        )
        
        # Calculate weight loss
        batch.calculate_weight_loss()
        
        db.session.add(batch)
        db.session.commit()
        
        flash('Roast batch created successfully!', 'success')
        return redirect(url_for('roast.batch_detail', id=batch.id))
    
    profiles = RoastProfile.query.filter_by(is_active=True).all()
    return render_template('roast/batch_form.html', batch=None, profiles=profiles)


@bp.route('/batches/<int:id>')
@login_required
def batch_detail(id):
    """View roast batch details."""
    batch = RoastBatch.query.get_or_404(id)
    return render_template('roast/batch_detail.html', batch=batch)
