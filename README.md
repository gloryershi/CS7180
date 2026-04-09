# VetCheck — Animal Symptom Checker

A Streamlit + Flask application for predicting animal diseases based on observed symptoms.  
Currently uses **placeholder models**; swap in real `.joblib` files when ready.

---

## Project Structure

```
ML_SymptomChecker/
├── flask_backend/
│   ├── app.py                  # Flask API (port 5001) --> we use 5001 to avoid conflicts
│   └── models/
│       └── __init__.py         # Placeholder predict_dog / predict_cat / predict_livestock
│
├── streamlit_app/
│   ├── app.py                  # Main entry point (st.navigation)
│   ├── pages/
│   │   ├── home.py             # Landing page + animal selector
│   │   ├── symptom_checker.py  # Symptom form
│   │   ├── results.py          # Prediction results
│   │   ├── about_model.py      # Model metadata
│   │   └── vet_disclaimer.py   # Disclaimer
│   └── utils/
│       ├── api.py              # Flask API client
│       └── styles.py           # Shared CSS + helper components
│
├── requirements.txt
└── README.md
```

---

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Flask backend (Terminal 1)
```bash
python flask_backend/app.py
# → running on http://localhost:5001
```

### 3. Start the Streamlit frontend (Terminal 2)
```bash
streamlit run streamlit_app/app.py
# → opens http://localhost:8501
```

---

## Docker usage

You can run the full stack (Flask backend + Streamlit frontend) in Docker.

### 1. Build the image

```bash
docker build -t ml_symptom_checker .
```

- **What it does**: Reads the `Dockerfile`, installs dependencies from `requirements.txt`, copies the project into the image, and creates a local Docker image named `ml_symptom_checker`.

### 2. Run the app (Streamlit + Flask)

```bash
docker run -p 8501:8501 -p 5001:5001 ml_symptom_checker
```

- **What it does**: Starts a container from the `ml_symptom_checker` image, runs `streamlit_app/app.py` on port `8501`, and exposes the Flask backend on port `5001` inside the container.
- **Access**:
  - Streamlit UI: `http://localhost:8501`
  - Flask API: `http://localhost:5001`

### 3. Run only the Flask backend in Docker (optional)

```bash
docker run -p 5001:5001 ml_symptom_checker \
  flask --app flask_backend/app.py run --host=0.0.0.0 --port=5001
```

- **What it does**: Overrides the default Streamlit CMD and runs the Flask dev server inside the container, still listening on port `5001`.

### 4. Save / load the image as a `.tar` (optional)

```bash
# Save image to tarball
docker save -o ml_symptom_checker.tar ml_symptom_checker

# Load image from tarball
docker load -i ml_symptom_checker.tar
```

- **What it does**: `docker save` exports the image as a `.tar` file (useful for sharing or submitting), and `docker load` imports it back on another machine.

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/symptoms/<animal>` | Symptom list for dog / cat / livestock |
| POST | `/api/predict` | `{"animal": "dog", "symptoms": [...]}` |
| GET | `/api/metadata` | All model metadata |
| GET | `/api/metadata/<animal>` | Metadata for one animal |

---

## Disclaimer

This tool is for **educational and development use only**.  
It does not provide veterinary diagnoses. Always consult a licensed veterinarian.
