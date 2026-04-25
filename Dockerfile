# Use a modern, minimal, secure base image
FROM python:3.12-slim AS base

# Ensure no cache and install securely
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY tests ./tests

# Non-root user for security
RUN useradd -m secureuser
USER secureuser

EXPOSE 8080
CMD ["python", "-m", "app.main"]

