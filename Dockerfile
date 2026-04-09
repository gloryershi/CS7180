FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (if you add any compiled libs, update this)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency list and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Streamlit configuration for running inside Docker
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ENABLE_WEBBROWSER=false \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    FLASK_APP=flask_backend/app.py \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_RUN_PORT=5001

# Expose both the Streamlit and Flask ports
EXPOSE 8501 5001

# By default, run the Streamlit app.
# You can override this at runtime to run the Flask backend instead, e.g.:
#   docker run ... ml_symptom_checker flask --app flask_backend/app.py run
CMD ["streamlit", "run", "streamlit_app/app.py"]

