# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy files
COPY . /app/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the correct port
EXPOSE 10000

# Run the app with Gunicorn (replace `run` with your filename without `.py`)
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "run:app"]
