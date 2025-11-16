#!/bin/sh
set -e

# Ensure Flask knows how to locate the application factory
export FLASK_APP="app:create_app"

# Run migrations every time the container starts.
echo "Running database migrations..."
flask db upgrade

# Optionally seed data when RUN_SEED=true
if [ "${RUN_SEED:-false}" = "true" ]; then
  echo "Seeding database with sample data..."
  python seed_data.py
fi

echo "Starting application: $*"
exec "$@"
