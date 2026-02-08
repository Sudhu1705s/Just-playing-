FROM python:3.10.17-slim

WORKDIR /app

COPY requirements.txt .

# Install dependencies, including build tools and FFmpeg
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        python3-dev && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get remove --purge -y \
        build-essential \
        gcc \
        python3-dev && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY . .

CMD ["python3", "main.py"]