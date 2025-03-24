# Use Ubuntu as the base image
FROM ubuntu:22.04

# Set the working directory
WORKDIR /app

# Install system dependencies and Python
RUN apt-get update && apt-get install -y \
    python3 python3-pip curl wget unzip \
    libglib2.0-0 libnss3 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libdbus-1-3 libxcomposite1 libxdamage1 libxrandr2 \
    libgbm1 libgtk-3-0 libasound2 libxshmfence1 \
    && rm -rf /var/lib/apt/lists/*

# Install Playwright and Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Install Playwright browsers and dependencies
RUN pip3 install playwright && playwright install && playwright install-deps

# Copy the app's code
COPY . .

# Expose the port Railway uses
EXPOSE 8080

# Run the Flask app
CMD ["python3", "main.py"]
