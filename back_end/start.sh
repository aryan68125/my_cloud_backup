#!/bin/sh
set -e

echo "Waiting for PostgreSQL..."
until python3 -c "
import socket, sys, os
try:
    socket.create_connection(
        (os.environ.get('POSTGRES_HOST', 'postgres'),
         int(os.environ.get('POSTGRES_PORT', '5432'))),
        timeout=2
    )
    sys.exit(0)
except Exception as e:
    print('Not ready:', e, flush=True)
    sys.exit(1)
"; do
    sleep 2
done

echo "PostgreSQL is ready."
alembic upgrade head
python back_end_initialization/seed_data.py
exec uvicorn main:app --host 0.0.0.0 --port 8000
