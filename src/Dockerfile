# Base image
FROM python:3.12.8-slim-bullseye

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Create entrypoint to run run_all.py
ENTRYPOINT ["python", "run_all.py"]

# Alternative command for FastAPI - can be overridden with docker run
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
