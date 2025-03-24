# Use an official Playwright image with necessary dependencies
FROM mcr.microsoft.com/playwright/python:v1.51.1-jammy

# Set the working directory inside the container
WORKDIR /app

# Copy your project files into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure Playwright browsers and dependencies are installed
RUN playwright install --with-deps

# Expose the correct port
EXPOSE 8080

# Run your Flask application
CMD ["python", "main.py"]
