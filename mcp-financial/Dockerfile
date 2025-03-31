# Use official Python image
FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy all project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the MCP default port
EXPOSE 8000

# Run MCP server
CMD ["python", "financial_history.py"]
