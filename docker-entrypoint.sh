#!/bin/sh
# Entrypoint script for web container
# Runs migrations before starting the app

set -e

echo "Waiting for database to be ready..."
sleep 5

echo "Running database migrations..."

# Initialize migrations if not exists
if [ ! -d "migrations" ]; then
    echo "Initializing Flask-Migrate..."
    flask db init
fi

# Create migration
echo "Creating migration..."
flask db migrate -m "Auto migration" || echo "No new migrations to create"

# Apply migrations
echo "Applying migrations..."
flask db upgrade

echo "✓ Database migrations completed!"
echo "Starting application..."

exec "$@"
