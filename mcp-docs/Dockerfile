# Use official Python image
FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy the requirements.txt from the parent directory on your host
COPY ../requirements.txt ./requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Then copy the rest of your application code (optional)
COPY . .

# Expose the MCP default port
EXPOSE 8000

# Run MCP server
CMD ["python", "doc_search.py"]
