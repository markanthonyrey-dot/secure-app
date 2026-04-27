# Dockerfile
# Security: Use official minimal base image with specific version
FROM python:3.11-slim-bookworm

# Security: Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    FLASK_APP=app.main \
    FLASK_HOST=0.0.0.0 \
    FLASK_PORT=5000

# Security: Create non-root user
RUN groupadd --gid 1000 appgroup && \
    useradd --uid 1000 --gid appgroup --shell /bin/false appuser

# Security: Set working directory
WORKDIR /app

# Security: Copy requirements first for better layer caching
COPY requirements.txt .

# Security: Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Security: Copy application code
COPY app/ ./app/

# Security: Change ownership to non-root user
RUN chown -R appuser:appgroup /app

# Security: Switch to non-root user
USER appuser

# Security: Expose only necessary port
EXPOSE 5000

# Security: Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# Security: Use exec form for better signal handling
CMD ["python", "-m", "flask", "--app", "app.main", "run", "--host=0.0.0.0", "--port=5000"]
