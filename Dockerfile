# 1. Base Image
FROM python:3.13-slim

# 2. Python Environment Optimizations
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. Create a non-root system user and group for security
RUN groupadd --system appgroup && \
    useradd --system --gid appgroup --create-home appuser

# 4. Set working directory
WORKDIR /app

# 5. Leverage Layer Caching for dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy application source code
COPY . .

# 7. Initialize the database (Baked into the image for lab purposes)
RUN python init_db.py

# 8. Transfer ownership of the application files to the non-root user
RUN chown -R appuser:appgroup /app

# 9. Switch from root to the restricted user
USER appuser

# 10. Document the port
EXPOSE 5000

# 11. Docker-native Healthcheck (Will be superseded by K8s later)
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# 12. Execution
CMD ["python", "app.py"]