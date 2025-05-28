from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), nullable=False)  # 'Planner' or 'Technician'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    work_orders = db.relationship('WorkOrder', backref='assigned_technician', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(120), nullable=False)
    manufacturer = db.Column(db.String(120))
    model_number = db.Column(db.String(120))
    serial_number = db.Column(db.String(120), unique=True)
    installation_date = db.Column(db.Date)
    pm_frequency_notes = db.Column(db.Text)
    next_pm_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    work_orders = db.relationship('WorkOrder', backref='asset', lazy='dynamic')

    def __repr__(self):
        return f'<Asset {self.name}>'

class WorkOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    work_order_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # Preventive, Corrective, Emergency
    status = db.Column(db.String(20), nullable=False, default='Open')  # Open, In Progress, On Hold, Completed, Cancelled
    description = db.Column(db.Text)
    priority = db.Column(db.String(20), nullable=False, default='Medium')  # High, Medium, Low
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.Date)
    assigned_technician_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    completion_notes = db.Column(db.Text)
    completed_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<WorkOrder {self.work_order_id}>'

    @staticmethod
    def generate_work_order_id():
        """Generate a unique work order ID in the format: WO-YYYYMMDD-XXXX"""
        date_str = datetime.utcnow().strftime('%Y%m%d')
        last_wo = WorkOrder.query.filter(
            WorkOrder.work_order_id.like(f'WO-{date_str}-%')
        ).order_by(WorkOrder.work_order_id.desc()).first()

        if last_wo:
            last_number = int(last_wo.work_order_id.split('-')[-1])
            new_number = last_number + 1
        else:
            new_number = 1

        return f'WO-{date_str}-{new_number:04d}'
