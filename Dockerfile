# Build stage
FROM python:3.12.9-slim

WORKDIR /app

# Install build dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

CMD alembic upgrade head; python src/main.py