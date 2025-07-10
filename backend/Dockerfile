FROM ghcr.io/astral-sh/uv:python3.11-alpine

ENV ENV_MODE=production
WORKDIR /app

RUN apk add --no-cache curl git bash

# Install Python dependencies
COPY pyproject.toml uv.lock ./
ENV UV_LINK_MODE=copy
RUN --mount=type=cache,target=/root/.cache/uv uv sync --locked --quiet

# Copy application code
COPY . .

# Make start script executable
COPY start.sh ./
RUN chmod +x start.sh

# Default environment variables for Render
ENV WORKERS=4
ENV THREADS=2
ENV WORKER_CONNECTIONS=1000
ENV PYTHONPATH=/app
ENV PORT=8000

EXPOSE $PORT

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:$PORT/api/health || exit 1

# Use start script
CMD ["./start.sh"]
