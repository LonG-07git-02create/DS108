# ==================================================
# Base Image
# ==================================================
FROM python:3.10-slim

# ==================================================
# Work Directory
# ==================================================
WORKDIR /workspace

# ==================================================
# System Dependencies
# ==================================================
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ==================================================
# Copy Requirements
# ==================================================
COPY requirement.txt .

# ==================================================
# Install Python Packages
# ==================================================
RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirement.txt

# ==================================================
# Copy Project
# ==================================================
COPY . .

# ==================================================
# Streamlit Config
# ==================================================
ENV PYTHONUNBUFFERED=1

ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# ==================================================
# Expose Port
# ==================================================
EXPOSE 8501

# ==================================================
# Health Check
# ==================================================
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# ==================================================
# Run App
# ==================================================
CMD ["streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]