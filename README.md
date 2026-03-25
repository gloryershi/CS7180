# VetCheck — Animal Symptom Checker

A Streamlit + Flask application for predicting animal diseases based on observed symptoms.  
Currently uses **placeholder models**; swap in real `.joblib` files when ready.

---

## Project Structure

```
ML_SymptomChecker/
├── flask_backend/
│   ├── app.py                  # Flask API (port 5000)
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

## Swapping in Real Models

Edit `flask_backend/models/__init__.py`.  
Replace the `_placeholder_result()` call in each function with your trained model:

```python
import joblib

_dog_model = joblib.load("flask_backend/models/dog_model.joblib")

def predict_dog(symptoms: list[str]) -> dict:
    features = vectorize(symptoms)          # your vectoriser
    label    = _dog_model.predict([features])[0]
    prob     = _dog_model.predict_proba([features])[0].max()
    return {
        "animal":     "dog",
        "condition":  label,
        "confidence": round(float(prob), 2),
        "urgency":    map_urgency(label),   # your urgency mapping
        "why":        "...",
        "next_steps": [...],
        "matched_symptoms": symptoms,
        "red_flags":  [...],
        "model_version": "1.0.0",
        "is_placeholder": False,
    }
```

Update `MODEL_METADATA` in the same file with real version info and accuracy.

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
