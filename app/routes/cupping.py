"""Cupping form routes."""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import CuppingSession, RoastBatch

bp = Blueprint('cupping', __name__, url_prefix='/cupping')


@bp.route('/')
@login_required
def index():
    """List cupping sessions."""
    page = request.args.get('page', 1, type=int)
    sessions = CuppingSession.query.order_by(
        CuppingSession.session_date.desc()
    ).paginate(page=page, per_page=20, error_out=False)
    return render_template('cupping/index.html', sessions=sessions)


@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_session():
    """Create new cupping session."""
    if request.method == 'POST':
        session = CuppingSession(
            evaluator_id=current_user.id,
            batch_id=int(request.form.get('batch_id')) if request.form.get('batch_id') else None,
            fragrance_aroma=float(request.form.get('fragrance_aroma', 0)),
            flavor=float(request.form.get('flavor', 0)),
            aftertaste=float(request.form.get('aftertaste', 0)),
            acidity=float(request.form.get('acidity', 0)),
            body=float(request.form.get('body', 0)),
            balance=float(request.form.get('balance', 0)),
            sweetness=float(request.form.get('sweetness', 10)),
            clean_cup=float(request.form.get('clean_cup', 10)),
            uniformity=float(request.form.get('uniformity', 10)),
            overall=float(request.form.get('overall', 0)),
            defects=int(request.form.get('defects', 0)),
            defect_intensity=int(request.form.get('defect_intensity', 0)),
            tasting_notes=request.form.get('tasting_notes')
        )
        session.calculate_scores()
        db.session.add(session)
        db.session.commit()
        flash(f'Cupping session created! Final score: {session.final_score}', 'success')
        return redirect(url_for('cupping.session_detail', id=session.id))
    
    batches = RoastBatch.query.order_by(RoastBatch.roast_date.desc()).limit(50).all()
    return render_template('cupping/form.html', session=None, batches=batches)


@bp.route('/<int:id>')
@login_required
def session_detail(id):
    """View cupping session details."""
    session = CuppingSession.query.get_or_404(id)
    return render_template('cupping/detail.html', session=session)
