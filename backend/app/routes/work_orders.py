from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app import db
from app.models import WorkOrder, Asset, User
from app.forms import WorkOrderForm, WorkOrderUpdateForm
from datetime import datetime

work_orders_bp = Blueprint('work_orders', __name__)

@work_orders_bp.route('/')
@work_orders_bp.route('/index')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', None)
    type_filter = request.args.get('type', None)

    # Base query
    query = WorkOrder.query

    # Apply filters
    if status_filter and status_filter != 'All':
        query = query.filter(WorkOrder.status == status_filter)
    if type_filter and type_filter != 'All':
        query = query.filter(WorkOrder.type == type_filter)

    # Order by creation date, newest first
    query = query.order_by(WorkOrder.creation_date.desc())

    # Paginate results
    work_orders = query.paginate(
        page=page,
        per_page=current_app.config['WORK_ORDERS_PER_PAGE'],
        error_out=False
    )

    return render_template('work_orders/index.html',
                         title='Work Orders',
                         work_orders=work_orders,
                         status_filter=status_filter,
                         type_filter=type_filter)

@work_orders_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_work_order():
    form = WorkOrderForm()
    
    if form.validate_on_submit():
        work_order = WorkOrder(
            work_order_id=WorkOrder.generate_work_order_id(),
            asset_id=form.asset_id.data,
            type=form.type.data,
            status=form.status.data,
            description=form.description.data,
            priority=form.priority.data,
            due_date=form.due_date.data,
            assigned_technician_id=form.assigned_technician_id.data if form.assigned_technician_id.data != 0 else None
        )
        
        try:
            db.session.add(work_order)
            db.session.commit()
            flash('Work order has been created successfully.', 'success')
            return redirect(url_for('work_orders.view_work_order', work_order_id=work_order.id))
        except Exception as e:
            db.session.rollback()
            flash('Error creating work order. Please try again.', 'danger')
            return redirect(url_for('work_orders.add_work_order'))
    
    return render_template('work_orders/add_work_order.html',
                         title='Create Work Order',
                         form=form)

@work_orders_bp.route('/<int:work_order_id>')
@login_required
def view_work_order(work_order_id):
    work_order = WorkOrder.query.get_or_404(work_order_id)
    return render_template('work_orders/view_work_order.html',
                         title=f'Work Order - {work_order.work_order_id}',
                         work_order=work_order)

@work_orders_bp.route('/<int:work_order_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_work_order(work_order_id):
    work_order = WorkOrder.query.get_or_404(work_order_id)
    
    # Use different form based on user role
    if current_user.role == 'Technician':
        form = WorkOrderUpdateForm(obj=work_order)
    else:
        form = WorkOrderForm(obj=work_order)
    
    if form.validate_on_submit():
        try:
            # Update work order fields
            form.populate_obj(work_order)
            
            # If status changed to 'Completed', set completion date
            if work_order.status == 'Completed' and not work_order.completed_date:
                work_order.completed_date = datetime.utcnow()
            
            work_order.updated_at = datetime.utcnow()
            
            db.session.commit()
            flash('Work order has been updated successfully.', 'success')
            return redirect(url_for('work_orders.view_work_order', work_order_id=work_order.id))
        except Exception as e:
            db.session.rollback()
            flash('Error updating work order. Please try again.', 'danger')
    
    return render_template('work_orders/edit_work_order.html',
                         title=f'Edit Work Order - {work_order.work_order_id}',
                         form=form,
                         work_order=work_order)

@work_orders_bp.route('/<int:work_order_id>/delete', methods=['POST'])
@login_required
def delete_work_order(work_order_id):
    if current_user.role != 'Planner':
        flash('Only planners can delete work orders.', 'danger')
        return redirect(url_for('work_orders.view_work_order', work_order_id=work_order_id))
    
    work_order = WorkOrder.query.get_or_404(work_order_id)
    
    try:
        db.session.delete(work_order)
        db.session.commit()
        flash('Work order has been deleted successfully.', 'success')
        return redirect(url_for('work_orders.index'))
    except Exception as e:
        db.session.rollback()
        flash('Error deleting work order. Please try again.', 'danger')
        return redirect(url_for('work_orders.view_work_order', work_order_id=work_order_id))

@work_orders_bp.route('/search')
@login_required
def search_work_orders():
    query = request.args.get('q', '')
    if query:
        work_orders = WorkOrder.query.filter(
            (WorkOrder.work_order_id.ilike(f'%{query}%')) |
            (WorkOrder.description.ilike(f'%{query}%')) |
            (WorkOrder.completion_notes.ilike(f'%{query}%'))
        ).all()
    else:
        work_orders = []
    
    return render_template('work_orders/search.html',
                         title='Search Work Orders',
                         work_orders=work_orders,
                         query=query)
