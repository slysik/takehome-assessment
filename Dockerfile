# Multi-Stage Dockerfile for Multi-Agent Earnings Analyzer

# Stage 1: Builder
FROM python:3.11-slim as builder

# Set working directory
WORKDIR /app

# Suppress debconf warnings during package installation
ENV DEBIAN_FRONTEND=noninteractive
# Suppress pip warnings about running as root
ENV PIP_ROOT_USER_ACTION=ignore
# Disable pip version check notice
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Suppress debconf warnings during package installation
ENV DEBIAN_FRONTEND=noninteractive
# Suppress pip warnings about running as root
ENV PIP_ROOT_USER_ACTION=ignore
# Disable pip version check notice
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Create non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app

# Copy installed packages from builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Add build timestamp to bust cache
ARG BUILD_TIME=unknown
RUN echo "Build timestamp: $BUILD_TIME" && echo "$BUILD_TIME" > /.buildtime
LABEL build.timestamp=$BUILD_TIME

# Copy application code (with explicit --chown to avoid caching issues)
COPY --chown=appuser:appuser . /app

# Verify copy was successful
RUN ls -la /app/src/agents/sentiment.py && head -5 /app/src/agents/sentiment.py

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
ENV HOST=0.0.0.0
ENV PYTHONPATH=/app

# Switch to non-root user
USER appuser

# Expose application port
EXPOSE 8000

# Add health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Define the command to run your application
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
