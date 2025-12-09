"""Inventory management routes."""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import GreenBeanInventory, RoastedCoffeeInventory, InventoryTransaction
from datetime import datetime

bp = Blueprint('inventory', __name__, url_prefix='/inventory')


@bp.route('/')
@login_required
def index():
    """Inventory overview."""
    green_beans = GreenBeanInventory.query.filter_by(is_active=True).all()
    roasted_coffee = RoastedCoffeeInventory.query.filter_by(is_active=True).all()
    return render_template('inventory/index.html', 
                         green_beans=green_beans,
                         roasted_coffee=roasted_coffee)


@bp.route('/green-beans/new', methods=['GET', 'POST'])
@login_required
def new_green_bean():
    """Add new green bean inventory."""
    if request.method == 'POST':
        bean = GreenBeanInventory(
            name=request.form.get('name'),
            variety=request.form.get('variety'),
            origin=request.form.get('origin'),
            region=request.form.get('region'),
            processing_method=request.form.get('processing_method'),
            current_stock=float(request.form.get('current_stock', 0)),
            unit_cost=float(request.form.get('unit_cost', 0)),
            supplier_name=request.form.get('supplier_name'),
            low_stock_threshold=float(request.form.get('low_stock_threshold', 10))
        )
        bean.check_low_stock()
        db.session.add(bean)
        db.session.commit()
        flash('Green bean inventory added!', 'success')
        return redirect(url_for('inventory.index'))
    
    return render_template('inventory/green_bean_form.html', bean=None)


@bp.route('/roasted-coffee/new', methods=['GET', 'POST'])
@login_required
def new_roasted_coffee():
    """Add new roasted coffee inventory."""
    if request.method == 'POST':
        coffee = RoastedCoffeeInventory(
            sku=request.form.get('sku'),
            product_name=request.form.get('product_name'),
            roast_level=request.form.get('roast_level'),
            current_stock=float(request.form.get('current_stock', 0)),
            unit_cost=float(request.form.get('unit_cost', 0)),
            selling_price=float(request.form.get('selling_price', 0))
        )
        db.session.add(coffee)
        db.session.commit()
        flash('Roasted coffee inventory added!', 'success')
        return redirect(url_for('inventory.index'))
    
    return render_template('inventory/roasted_coffee_form.html', coffee=None)
