#!/bin/bash
# Wait for PostgreSQL to become available
./wait-for-it.sh ${DB_HOSTNAME}:5432 --timeout=30 --strict -- echo "Banco de dados está pronto."

# Now start the application
PORT=${PORT:-9999}
exec python ./app/main.py $PORT
