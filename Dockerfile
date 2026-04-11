FROM python:3.11-slim

WORKDIR /app

# Install Python dependencies separately for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application source
COPY . .

# Runtime configuration for Streamlit + Flask inside the container
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ENABLE_WEBBROWSER=false \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    FLASK_APP=flask_backend/app.py \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_RUN_PORT=5001

EXPOSE 8501 5001

# Default to Streamlit; override CMD at runtime to run Flask only
CMD ["streamlit", "run", "streamlit_app/app.py"]

