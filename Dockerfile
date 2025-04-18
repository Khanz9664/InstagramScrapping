# Use a Python base image with a slim version to minimize the image size
FROM python:3.11-slim

# Update package lists and install common dependencies
RUN apt-get update && apt-get install -y \
    ca-certificates \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install the Playwright dependencies
RUN apt-get update && apt-get install -y \
    gstreamer1.0-plugins-base \
    libgtk-4-1 \
    libgraphene-1.0-0 \
    libgstreamer-gl1.0-0 \
    libavif15 \
    libenchant-2-2 \
    libsecret-1-0 \
    libmanette-0.2-0 \
    libgles2 \
    libxss1 \
    libappindicator3-1 \
    libasound2 \
    libnss3 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and browsers
RUN pip install playwright && playwright install

# Copy the rest of the application code into the container
COPY . .

# Expose the port that the app will run on
EXPOSE 10000

# Command to run the Flask app with gunicorn
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:10000"]
