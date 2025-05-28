from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app import db
from app.models import Asset, WorkOrder
from app.forms import AssetForm
from datetime import datetime

assets_bp = Blueprint('assets', __name__)

@assets_bp.route('/')
@assets_bp.route('/index')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    assets = Asset.query.order_by(Asset.name).paginate(
        page=page, 
        per_page=current_app.config['ASSETS_PER_PAGE'],
        error_out=False
    )
    
    # Get work order counts for each asset
    asset_wo_counts = {}
    for asset in assets.items:
        open_wo_count = WorkOrder.query.filter_by(
            asset_id=asset.id
        ).filter(
            WorkOrder.status.in_(['Open', 'In Progress', 'On Hold'])
        ).count()
        asset_wo_counts[asset.id] = open_wo_count
    
    return render_template('assets/index.html',
                         title='Assets',
                         assets=assets,
                         asset_wo_counts=asset_wo_counts)

@assets_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_asset():
    form = AssetForm()
    if form.validate_on_submit():
        asset = Asset(
            name=form.name.data,
            description=form.description.data,
            location=form.location.data,
            manufacturer=form.manufacturer.data,
            model_number=form.model_number.data,
            serial_number=form.serial_number.data,
            installation_date=form.installation_date.data,
            pm_frequency_notes=form.pm_frequency_notes.data,
            next_pm_date=form.next_pm_date.data
        )
        
        try:
            db.session.add(asset)
            db.session.commit()
            flash('Asset has been added successfully.', 'success')
            return redirect(url_for('assets.view_asset', asset_id=asset.id))
        except Exception as e:
            db.session.rollback()
            flash('Error adding asset. Please try again.', 'danger')
            return redirect(url_for('assets.add_asset'))
    
    return render_template('assets/add_asset.html',
                         title='Add Asset',
                         form=form)

@assets_bp.route('/<int:asset_id>')
@login_required
def view_asset(asset_id):
    asset = Asset.query.get_or_404(asset_id)
    
    # Get related work orders
    work_orders = WorkOrder.query.filter_by(asset_id=asset_id)\
        .order_by(WorkOrder.creation_date.desc())\
        .limit(5)\
        .all()
    
    return render_template('assets/view_asset.html',
                         title=f'Asset - {asset.name}',
                         asset=asset,
                         work_orders=work_orders)

@assets_bp.route('/<int:asset_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_asset(asset_id):
    asset = Asset.query.get_or_404(asset_id)
    form = AssetForm(obj=asset)
    
    if form.validate_on_submit():
        try:
            # Update asset fields
            form.populate_obj(asset)
            asset.updated_at = datetime.utcnow()
            
            db.session.commit()
            flash('Asset has been updated successfully.', 'success')
            return redirect(url_for('assets.view_asset', asset_id=asset.id))
        except Exception as e:
            db.session.rollback()
            flash('Error updating asset. Please try again.', 'danger')
    
    return render_template('assets/edit_asset.html',
                         title=f'Edit Asset - {asset.name}',
                         form=form,
                         asset=asset)

@assets_bp.route('/<int:asset_id>/delete', methods=['POST'])
@login_required
def delete_asset(asset_id):
    asset = Asset.query.get_or_404(asset_id)
    
    # Check if there are any work orders associated with this asset
    if WorkOrder.query.filter_by(asset_id=asset_id).first():
        flash('Cannot delete asset with associated work orders.', 'danger')
        return redirect(url_for('assets.view_asset', asset_id=asset_id))
    
    try:
        db.session.delete(asset)
        db.session.commit()
        flash('Asset has been deleted successfully.', 'success')
        return redirect(url_for('assets.index'))
    except Exception as e:
        db.session.rollback()
        flash('Error deleting asset. Please try again.', 'danger')
        return redirect(url_for('assets.view_asset', asset_id=asset_id))

@assets_bp.route('/search')
@login_required
def search_assets():
    query = request.args.get('q', '')
    if query:
        assets = Asset.query.filter(
            (Asset.name.ilike(f'%{query}%')) |
            (Asset.description.ilike(f'%{query}%')) |
            (Asset.location.ilike(f'%{query}%')) |
            (Asset.serial_number.ilike(f'%{query}%'))
        ).all()
    else:
        assets = []
    
    return render_template('assets/search.html',
                         title='Search Assets',
                         assets=assets,
                         query=query)
