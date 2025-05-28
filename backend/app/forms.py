from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, DateField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('Planner', 'Planner'), ('Technician', 'Technician')],
                      validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class AssetForm(FlaskForm):
    name = StringField('Asset Name', validators=[DataRequired(), Length(max=120)])
    description = TextAreaField('Description')
    location = StringField('Location', validators=[DataRequired(), Length(max=120)])
    manufacturer = StringField('Manufacturer', validators=[Optional(), Length(max=120)])
    model_number = StringField('Model Number', validators=[Optional(), Length(max=120)])
    serial_number = StringField('Serial Number', validators=[Optional(), Length(max=120)])
    installation_date = DateField('Installation Date', validators=[Optional()])
    pm_frequency_notes = TextAreaField('PM Frequency Notes')
    next_pm_date = DateField('Next PM Date', validators=[Optional()])
    submit = SubmitField('Submit')

class WorkOrderForm(FlaskForm):
    asset_id = SelectField('Asset', coerce=int, validators=[DataRequired()])
    type = SelectField('Type', choices=[
        ('Preventive', 'Preventive'),
        ('Corrective', 'Corrective'),
        ('Emergency', 'Emergency')
    ], validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    priority = SelectField('Priority', choices=[
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low')
    ], default='Medium', validators=[DataRequired()])
    status = SelectField('Status', choices=[
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('On Hold', 'On Hold'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled')
    ], default='Open', validators=[DataRequired()])
    due_date = DateField('Due Date', validators=[Optional()])
    assigned_technician_id = SelectField('Assigned Technician', coerce=int, validators=[Optional()])
    completion_notes = TextAreaField('Completion Notes')
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(WorkOrderForm, self).__init__(*args, **kwargs)
        from app.models import Asset, User
        # Populate asset choices
        self.asset_id.choices = [(a.id, a.name) for a in Asset.query.order_by('name')]
        # Populate technician choices
        techs = User.query.filter_by(role='Technician').order_by('username').all()
        self.assigned_technician_id.choices = [(0, 'Unassigned')] + [(t.id, t.username) for t in techs]

class WorkOrderUpdateForm(WorkOrderForm):
    status = SelectField('Status', choices=[
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('On Hold', 'On Hold'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled')
    ], validators=[DataRequired()])
    completion_notes = TextAreaField('Completion Notes', validators=[Optional()])
