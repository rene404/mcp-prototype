FROM python:3.12

WORKDIR /app

# Copy everything into the image
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make root project packages importable
ENV PYTHONPATH=/app
