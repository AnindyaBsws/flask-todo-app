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
RUN pip install --no-warn-script-location --root-user-action=ignore -r requirements.txt

# Expose the correct port
EXPOSE 10000

# Run the app with Gunicorn (replace `run` if your app is in a different file)
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "run:app"]
