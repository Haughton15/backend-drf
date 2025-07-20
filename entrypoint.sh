#!/bin/sh
if [ "$DATABASE" = "postgres" ]; then
    echo "Waiting for postgres..."
    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
        sleep 0.1
    done
    echo "PostgreSQL started"
fi

# Run migrations and apply initial SQL script
echo "Running migrations..."
python manage.py migrate

# Check if the init.sql file exists
echo "Applying init.sql..."
PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DB -f db/init.sql || { echo "Error: Failed to apply init.sql"; exit 1; }

# Run tests
echo "Running tests..."
python manage.py test || { echo "Error: Tests failed"; exit 1; }

echo "Starting Django server..."
exec "$@"