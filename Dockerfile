# Use the official Playwright image with all dependencies
FROM mcr.microsoft.com/playwright/python:v1.42.0-jammy

# Set working directory
WORKDIR /app

# Install system dependencies for scraping
RUN apt-get update && \
    apt-get install -y \
    python3-pip \
    libgirepository1.0-dev \
    libcairo2-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Install Playwright browsers and system dependencies
RUN playwright install --with-deps chromium

# Configure environment for headless browser
ENV DISPLAY=:99
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

# Optimize for Render's ephemeral storage
RUN mkdir -p /tmp/storage

# Set proper permissions
RUN chmod -R 755 /app

# Use the port Render expects
ENV PORT=8080
EXPOSE 8080

# Start the application with production settings
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--timeout", "600", "main:app"]
