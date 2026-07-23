# Use an official Python image
FROM python:3.13-slim

# Set working directory inside the container
WORKDIR /app

# Copy dependency file first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Initialize the database
RUN python init_db.py

# Expose Flask port
EXPOSE 5000

# Start the application
CMD ["python", "app.py"]