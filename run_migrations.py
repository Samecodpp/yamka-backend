"""
Database migration script for Docker deployment
Run this inside the web container to create/update database tables
"""
import os
import sys

def run_migrations():
    """Run Flask-Migrate commands"""
    print("=" * 60)
    print("DATABASE MIGRATION SCRIPT")
    print("=" * 60)

    # Check if migrations folder exists
    if not os.path.exists('migrations'):
        print("\n[1/3] Initializing Flask-Migrate...")
        ret = os.system('flask db init')
        if ret != 0:
            print("ERROR: Failed to initialize Flask-Migrate")
            return False
    else:
        print("\n[1/3] Flask-Migrate already initialized")

    # Create migration
    print("\n[2/3] Creating migration...")
    ret = os.system('flask db migrate -m "Auto migration"')
    if ret != 0:
        print("WARNING: Migration creation failed (this is OK if no changes detected)")

    # Apply migrations
    print("\n[3/3] Applying migrations to database...")
    ret = os.system('flask db upgrade')
    if ret != 0:
        print("ERROR: Failed to apply migrations")
        return False

    print("\n" + "=" * 60)
    print("✓ DATABASE MIGRATION COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    return True

if __name__ == '__main__':
    success = run_migrations()
    sys.exit(0 if success else 1)
