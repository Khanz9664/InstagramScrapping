# Use the official Playwright image with Python
FROM mcr.microsoft.com/playwright/python:v1.42.0-jammy

# Set working directory
WORKDIR /app

# Install system dependencies for gevent and Playwright
RUN apt-get update && \
    apt-get install -y \
    python3-pip \
    libevent-dev \          # Critical for gevent
    libglib2.0-0 \          # Playwright dependency
    libnss3 \               # Playwright dependency
    libnspr4 \              # Playwright dependency
    libatk1.0-0 \           # Accessibility toolkit
    libatk-bridge2.0-0 \    # AT-SPI bridge
    libcups2 \              # Printing support
    libdrm2 \               # Direct Rendering Manager
    libxkbcommon0 \         # Keyboard handling
    libxcomposite1 \        # X11 composite extension
    libxdamage1 \           # X11 damage extension
    libxfixes3 \            # X11 fixes extension
    libxrandr2 \            # X11 RandR extension
    libgbm1 \               # Graphics memory management
    libpango-1.0-0 \        # Text layout and rendering
    libcairo2 \             # Vector graphics library
    libasound2 \            # ALSA sound support
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for layer caching
COPY requirements.txt .

# Install Python dependencies
RUN python -m pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Install Playwright browsers
RUN playwright install --with-deps chromium

# Configure environment variables
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
ENV PORT=8080

# Expose the application port
EXPOSE 8080

# Verify gevent installation
RUN python -c "import gevent; print(f'Successfully installed gevent {gevent.__version__}')"

# Start Gunicorn with gevent worker
CMD ["gunicorn", \
    "--bind", "0.0.0.0:8080", \
    "--timeout", "300", \
    "--worker-class", "gevent", \
    "--workers", "1", \
    "--access-logfile", "-", \
    "main:application"]
