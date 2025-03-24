# Use the latest compatible Playwright image
FROM mcr.microsoft.com/playwright/python:latest-jammy

# Set the working directory
WORKDIR /app

# Copy the project files
COPY . .

# Install Python dependencies
RUN pip install -r requirements.txt

# Ensure Playwright browsers and system dependencies are installed
RUN playwright install && playwright install-deps

# Expose the correct port (use Railway's PORT)
EXPOSE 8080

# Run the Flask application
CMD ["python", "main.py"]
