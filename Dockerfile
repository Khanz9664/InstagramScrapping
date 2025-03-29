# Use this exact Dockerfile
FROM mcr.microsoft.com/playwright/python:v1.42.0-jammy

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN playwright install --with-deps chromium

ENV DISPLAY=:99
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
ENV PORT=8080

CMD ["gunicorn", \
    "--bind", "0.0.0.0:8080", \
    "--timeout", "300", \
    "--worker-class", "gevent", \
    "--workers", "1", \
    "--access-logfile", "-", \
    "main:application"]
