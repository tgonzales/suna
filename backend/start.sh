#!/bin/bash
set -e

echo "🚀 Starting Suna Backend..."

# Wait for dependencies (if any)
echo "⏳ Waiting for dependencies..."
sleep 5

# Initialize production settings
echo "🔧 Initializing production settings..."
if python init_production.py; then
    echo "✅ Production initialization completed"
else
    echo "⚠️  Production initialization failed, continuing anyway..."
fi

# Start the application
echo "🚀 Starting Gunicorn server..."
exec uv run gunicorn api:app \
  --workers ${WORKERS:-4} \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:${PORT:-8000} \
  --timeout 1800 \
  --graceful-timeout 600 \
  --keep-alive 1800 \
  --max-requests 0 \
  --max-requests-jitter 0 \
  --forwarded-allow-ips '*' \
  --worker-connections ${WORKER_CONNECTIONS:-2000} \
  --worker-tmp-dir /dev/shm \
  --preload \
  --log-level info \
  --access-logfile - \
  --error-logfile - \
  --capture-output \
  --enable-stdio-inheritance \
  --threads ${THREADS:-2}