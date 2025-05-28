# BCF Maintenance Optimization Platform

A comprehensive maintenance planning and tracking tool for biscuit manufacturing company (BCF). This platform helps maintenance planners manage equipment, schedule work orders, and track maintenance activities.

## Features

- **User Authentication**
  - Secure login and registration
  - Role-based access (Planner and Technician roles)
  - Protected routes for authenticated users

- **Asset Management**
  - Complete CRUD operations for maintenance assets
  - Track asset details including location, manufacturer info, and maintenance schedules
  - View asset maintenance history

- **Work Order Management**
  - Create and track different types of work orders (Preventive, Corrective, Emergency)
  - Automatic work order ID generation
  - Status tracking (Open, In Progress, On Hold, Completed, Cancelled)
  - Priority levels (High, Medium, Low)
  - Assign technicians to work orders
  - Track completion notes and maintenance history

## Technology Stack

- **Backend Framework:** Flask
- **Database:** SQLite (Development) / PostgreSQL (Production)
- **Frontend:** 
  - HTML templates with Jinja2
  - Bootstrap 5 for responsive design
  - Font Awesome icons
  - Custom CSS animations
- **Authentication:** Flask-Login
- **Forms:** Flask-WTF
- **Database ORM:** Flask-SQLAlchemy
- **Database Migrations:** Flask-Migrate

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd bcf-maintenance-platform
   ```

2. **Create and Activate Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the Database**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

5. **Create Environment Variables**
   Create a `.env` file in the root directory:
   ```
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///app.db
   ```

6. **Run the Application**
   ```bash
   python run.py
   ```
   The application will be available at `http://localhost:8000`

## Project Structure

```
backend/
├── app/
│   ├── __init__.py          # Flask app initialization
│   ├── models.py            # Database models
│   ├── forms.py             # WTForms definitions
│   ├── routes/              # Route blueprints
│   │   ├── auth.py         # Authentication routes
│   │   ├── assets.py       # Asset management routes
│   │   └── work_orders.py  # Work order management routes
│   └── templates/           # Jinja2 templates
│       ├── base.html       # Base template
│       ├── auth/           # Authentication templates
│       ├── assets/         # Asset management templates
│       └── work_orders/    # Work order templates
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
└── run.py                 # Application entry point
```

## Development Guidelines

1. **Database Migrations**
   When making changes to models:
   ```bash
   flask db migrate -m "Description of changes"
   flask db upgrade
   ```

2. **Running Tests**
   ```bash
   python -m pytest tests/
   ```

3. **Code Style**
   - Follow PEP 8 guidelines
   - Use meaningful variable and function names
   - Add docstrings to functions and classes
   - Keep functions focused and modular

## Production Deployment

1. **Database Configuration**
   - Set up PostgreSQL database
   - Update DATABASE_URL in environment variables
   - Run migrations

2. **Environment Variables**
   - Set FLASK_ENV=production
   - Set a strong SECRET_KEY
   - Configure logging settings

3. **Server Setup**
   - Use Gunicorn as WSGI server
   - Set up Nginx as reverse proxy
   - Configure SSL certificates
   - Set up monitoring and logging

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please contact the maintenance team or create an issue in the repository.
