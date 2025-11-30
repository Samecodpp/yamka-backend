#!/bin/bash
# Migration script for production deployment

set -e

echo "Starting database migration..."

# Initialize migrations folder if it doesn't exist
if [ ! -d "migrations" ]; then
    echo "Initializing Flask-Migrate..."
    flask db init
fi

# Create migration
echo "Creating migration..."
flask db migrate -m "Auto migration"

# Apply migration
echo "Applying migration to database..."
flask db upgrade

echo "✓ Database migration completed successfully!"
