# Use the latest Playwright image from GitHub's container registry
FROM ghcr.io/microsoft/playwright/python:v1.51.0

# Set the working directory inside the container
WORKDIR /app

# Copy your project files into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure Playwright browsers and dependencies are installed
RUN playwright install --with-deps

# Expose the Flask port (Render defaults to 8080)
EXPOSE 8080

# Start the Flask application
CMD ["python", "main.py"]
