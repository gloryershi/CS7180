"""Flask backend — exposes the prediction API consumed by the Streamlit frontend."""

from flask import Flask, request, jsonify
from flask_cors import CORS
from models import (
    SYMPTOMS,
    MODEL_METADATA,
    predict_dog,
    predict_cat,
    predict_livestock,
)

app = Flask(__name__)
CORS(app)

_PREDICTORS = {
    "dog": predict_dog,
    "cat": predict_cat,
    "livestock": predict_livestock,
}


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


# ---------------------------------------------------------------------------
# Symptom list for a given animal
# ---------------------------------------------------------------------------
@app.route("/api/symptoms/<animal>", methods=["GET"])
def get_symptoms(animal):
    animal = animal.lower()
    if animal not in SYMPTOMS:
        return jsonify({"error": f"Unknown animal '{animal}'"}), 400
    return jsonify({"animal": animal, "symptoms": SYMPTOMS[animal]})


# ---------------------------------------------------------------------------
# Prediction endpoint
# ---------------------------------------------------------------------------
@app.route("/api/predict", methods=["POST"])
def predict():
    body = request.get_json(silent=True) or {}
    animal = (body.get("animal") or "").lower().strip()
    symptoms = body.get("symptoms") or []

    # --- validation ---
    if animal not in _PREDICTORS:
        return jsonify({"error": "Field 'animal' must be 'dog', 'cat', or 'livestock'."}), 400
    if not isinstance(symptoms, list) or len(symptoms) == 0:
        return jsonify({"error": "Field 'symptoms' must be a non-empty list."}), 400

    result = _PREDICTORS[animal](symptoms)
    return jsonify(result)


# ---------------------------------------------------------------------------
# Model metadata
# ---------------------------------------------------------------------------
@app.route("/api/metadata", methods=["GET"])
def metadata():
    return jsonify(MODEL_METADATA)


@app.route("/api/metadata/<animal>", methods=["GET"])
def metadata_animal(animal):
    animal = animal.lower()
    if animal not in MODEL_METADATA:
        return jsonify({"error": f"Unknown animal '{animal}'"}), 400
    return jsonify(MODEL_METADATA[animal])


if __name__ == "__main__":
    app.run(port=5001, debug=True)
