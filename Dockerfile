# -------- STAGE 1: Build C++ --------
FROM ubuntu:24.04 AS builder

RUN apt-get update && apt-get install -y \
    cmake \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN mkdir build && cd build && \
    cmake .. && \
    make

# -------- STAGE 2: Runtime --------
FROM python:3.12-slim

WORKDIR /app

# Copy compiled binary
COPY --from=builder /app/build/sensor_simulator /app/build/sensor_simulator

# Copy Python code
COPY python/ ./python/

# Install dependencies (empty for now)
COPY python/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "python/process_sensor_data.py"]