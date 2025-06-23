# Use official Python image with version 3.11
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of your code
COPY . .

# Expose port for Render
EXPOSE 10000

# Run the app using gunicorn
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:10000"]
