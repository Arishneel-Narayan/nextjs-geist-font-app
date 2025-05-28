from app import create_app, db
from app.models import User, Asset, WorkOrder

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Provide useful objects for Flask shell."""
    return {
        'db': db,
        'User': User,
        'Asset': Asset,
        'WorkOrder': WorkOrder
    }

if __name__ == '__main__':
    with app.app_context():
        # Create database tables
        db.create_all()
    app.run(host='0.0.0.0', port=8000, debug=True)
