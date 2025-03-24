# Use Ubuntu with a compatible GLIBC version
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

# Set the working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Ensure Playwright browsers are installed
RUN playwright install

# Expose the port
EXPOSE 8080

# Run the Flask app
CMD ["python", "main.py"]
