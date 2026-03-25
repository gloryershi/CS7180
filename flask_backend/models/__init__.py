"""
Placeholder model functions for each animal type.
To upgrade: replace each function body with joblib.load(...) and model.predict().

Example swap-in:
    import joblib
    _model = joblib.load("dog_model.joblib")
    def predict_dog(symptoms):
        features = vectorize(symptoms)
        label = _model.predict([features])[0]
        prob  = _model.predict_proba([features])[0].max()
        return build_result("dog", label, prob)
"""

import random

# ---------------------------------------------------------------------------
# Shared symptom lists (replace / extend with your real feature vocabulary)
# ---------------------------------------------------------------------------
SYMPTOMS = {
    "dog": [
        "Fever", "Vomiting", "Diarrhea", "Lethargy", "Loss of appetite",
        "Itching", "Hair loss", "Coughing", "Limping", "Excessive thirst",
        "Bloating", "Seizures", "Eye discharge", "Nasal discharge",
        "Skin rash", "Weight loss", "Pale gums", "Difficulty breathing",
    ],
    "cat": [
        "Sneezing", "Eye discharge", "Nasal discharge", "Vomiting", "Diarrhea",
        "Lethargy", "Loss of appetite", "Itching", "Hair loss",
        "Straining to urinate", "Blood in urine", "Weight loss",
        "Excessive thirst", "Coughing", "Wheezing", "Hiding behavior",
        "Pale gums", "Difficulty breathing",
    ],
    "livestock": [
        "Fever", "Reduced milk production", "Limping", "Foot lesions",
        "Bloating", "Loss of appetite", "Diarrhea", "Coughing",
        "Nasal discharge", "Weight loss", "Lethargy", "Swollen udder",
        "Difficulty breathing", "Rough coat", "Pale gums",
        "Muscle tremors", "Abnormal feces",
    ],
}

# ---------------------------------------------------------------------------
# Minimal placeholder output builder
# ---------------------------------------------------------------------------
def _placeholder_result(animal: str, symptoms: list[str]) -> dict:
    """Returns a hardcoded placeholder result regardless of input."""
    return {
        "animal": animal,
        "condition": "Placeholder Condition — model not yet loaded",
        "confidence": round(random.uniform(0.55, 0.75), 2),
        "urgency": "medium",
        "why": "This is a placeholder prediction. The real model has not been loaded yet.",
        "next_steps": [
            "Consult a licensed veterinarian for a proper diagnosis.",
            "Keep a record of symptom onset and progression.",
        ],
        "matched_symptoms": symptoms,
        "red_flags": [],
        "model_version": "0.0.0-placeholder",
        "is_placeholder": True,
    }


# ---------------------------------------------------------------------------
# Public prediction functions — swap bodies when real models are ready
# ---------------------------------------------------------------------------
def predict_dog(symptoms: list[str]) -> dict:
    return _placeholder_result("dog", symptoms)


def predict_cat(symptoms: list[str]) -> dict:
    return _placeholder_result("cat", symptoms)


def predict_livestock(symptoms: list[str]) -> dict:
    return _placeholder_result("livestock", symptoms)


# ---------------------------------------------------------------------------
# Model metadata — update once real models are in place
# ---------------------------------------------------------------------------
MODEL_METADATA = {
    "dog": {
        "name": "Canine Disease Classifier",
        "version": "0.0.0-placeholder",
        "status": "placeholder",
        "training_status": "Awaiting real training data",
        "last_updated": "—",
        "accuracy": "N/A",
    },
    "cat": {
        "name": "Feline Disease Classifier",
        "version": "0.0.0-placeholder",
        "status": "placeholder",
        "training_status": "Awaiting real training data",
        "last_updated": "—",
        "accuracy": "N/A",
    },
    "livestock": {
        "name": "Livestock Disease Classifier",
        "version": "0.0.0-placeholder",
        "status": "placeholder",
        "training_status": "Awaiting real training data",
        "last_updated": "—",
        "accuracy": "N/A",
    },
}
