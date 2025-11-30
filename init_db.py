"""
Script to initialize database tables using Flask-Migrate
Run this once on the remote hosting to create all tables
"""
from application import create_app, db
from application.models import User, Device, DeviceReport, Pothole

app = create_app()

with app.app_context():
    print("Creating all database tables...")
    db.create_all()
    print("✓ Database tables created successfully!")

    # Verify tables were created
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"\nCreated tables: {', '.join(tables)}")
