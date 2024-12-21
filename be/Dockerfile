# Use the official Python image
FROM python:3.11 AS production
WORKDIR /app

# Copy FastAPI backend
COPY . /app/.

# Install dependencies for FastAPI
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expose the port for the backend
EXPOSE 8080

# Start the FastAPI application using Uvicorn
CMD ["fastapi", "run", "--host", "0.0.0.0", "--port", "8080"]
