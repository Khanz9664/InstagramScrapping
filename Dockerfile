# Use the official Playwright image that matches your version
FROM mcr.microsoft.com/playwright/python:v1.51.1-jammy

# Set the working directory
WORKDIR /app

# Copy the project files
COPY . .

# Install Python dependencies
RUN pip install -r requirements.txt

# Ensure Playwright browsers and dependencies are installed
RUN playwright install && playwright install-deps

# Expose the correct port
EXPOSE 8080

# Run the Flask application
CMD ["python", "main.py"]
