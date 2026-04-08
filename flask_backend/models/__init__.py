"""
Placeholder model functions for each animal type.
The cat pipeline loads `cat_label_encoder.joblib` (sklearn LabelEncoder) from this package;
wire `predict_cat` to your classifier and use `decode_cat_labels` on predicted indices.

Example swap-in for dog:
    import joblib
    _model = joblib.load("dog_model.joblib")
    def predict_dog(symptoms):
        features = vectorize(symptoms)
        label = _model.predict([features])[0]
        prob  = _model.predict_proba([features])[0].max()
        return build_result("dog", label, prob)
"""

import random
from pathlib import Path
from typing import Any, Optional

import joblib
import numpy as np
import pandas as pd

_MODELS_DIR = Path(__file__).resolve().parent
_CAT_MODEL_PATH = _MODELS_DIR / "cat_model.joblib"

_LIVESTOCK_MODEL_PATH = _MODELS_DIR / "livestock_model.joblib"
_LIVESTOCK_LE_PATH    = _MODELS_DIR / "livestock_label_encoder.joblib"

def _try_load_livestock() -> tuple:
    """Returns (model, label_encoder) or (None, None) if files missing."""
    if not _LIVESTOCK_MODEL_PATH.is_file():
        return None, None
    try:
        mdl = joblib.load(_LIVESTOCK_MODEL_PATH)
        le  = joblib.load(_LIVESTOCK_LE_PATH) if _LIVESTOCK_LE_PATH.is_file() else None
        return mdl, le
    except Exception:
        return None, None

LIVESTOCK_CLASSIFIER, LIVESTOCK_LABEL_ENCODER = _try_load_livestock()

_LIVESTOCK_SYMPTOM_COLS = [
    "blisters on gums", "blisters on hooves", "blisters on mouth",
    "blisters on tongue", "chest discomfort", "chills", "crackling sound",
    "depression", "difficulty walking", "fatigue", "lameness",
    "loss of appetite", "painless lumps", "shortness of breath",
    "sores on gums", "sores on hooves", "sores on mouth", "sores on tongue",
    "sweats", "swelling in abdomen", "swelling in extremities",
    "swelling in limb", "swelling in muscle", "swelling in neck",
]

_LIVESTOCK_ANIMAL_COLS = [
    "Animal_buffalo", "Animal_cow", "Animal_goat", "Animal_sheep",
]

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
        "Appetite_Loss", "Vomiting", "Diarrhea", "Coughing", "Labored_Breathing",
        "Lameness", "Skin_Lesions", "Nasal_Discharge","Eye_Discharge",
    ],
    "livestock": [
        "Blisters On Gums", "Blisters On Hooves", "Blisters On Mouth",
        "Blisters On Tongue", "Chest Discomfort", "Chills", "Crackling Sound",
        "Depression", "Difficulty Walking", "Fatigue", "Lameness",
        "Loss Of Appetite", "Painless Lumps", "Shortness Of Breath",
        "Sores On Gums", "Sores On Hooves", "Sores On Mouth", "Sores On Tongue",
        "Sweats", "Swelling In Abdomen", "Swelling In Extremities",
        "Swelling In Limb", "Swelling In Muscle", "Swelling In Neck",
    ],
}


# ---------------------------------------------------------------------------
# Feline label encoder (sklearn LabelEncoder persisted with joblib)
# ---------------------------------------------------------------------------
class CatLabelEncoderArtifact:
    """Loads `cat_label_encoder.joblib` beside this module for disease name ↔ index mapping."""

    __slots__ = ("_encoder",)

    def __init__(self) -> None:
        self._encoder: Optional[object] = None
        path = Path(__file__).resolve().parent / "cat_label_encoder.joblib"
        if path.is_file():
            try:
                self._encoder = joblib.load(path)
            except Exception:
                self._encoder = None

    @property
    def encoder(self) -> Optional[object]:
        return self._encoder

    def condition_names(self) -> list[str]:
        enc = self._encoder
        if enc is None or not hasattr(enc, "classes_"):
            return []
        return list(enc.classes_)

    def decode(self, y: Any) -> list:
        """Map encoded class indices to disease labels (for use after `predict` on the classifier)."""
        if self._encoder is None:
            raise RuntimeError("Cat label encoder is not loaded")
        return list(self._encoder.inverse_transform(y))


CAT_LABEL_ENCODER_ARTIFACT = CatLabelEncoderArtifact()
CAT_LABEL_ENCODER = CAT_LABEL_ENCODER_ARTIFACT.encoder


def cat_condition_names() -> list[str]:
    """Disease labels known to the trained cat encoder (empty if encoder missing)."""
    return CAT_LABEL_ENCODER_ARTIFACT.condition_names()


def decode_cat_labels(y: Any) -> list:
    """Decode integer predictions from the future cat classifier to readable condition names."""
    return CAT_LABEL_ENCODER_ARTIFACT.decode(y)


# Maps UI strings (lowercase) from SYMPTOMS["cat"] → (base binary columns, Symptom_i one-hot label).
# Base keys must match `cat_model.joblib` training columns Appetite_Loss … Eye_Discharge.
# Slot labels must match training one-hot names, e.g. "Eye Discharge", "Sneezing".
_CAT_UI_TO_TRAINING: dict[str, tuple[list[str], str]] = {
    "sneezing": ([], "Sneezing"),
    "eye discharge": (["Eye_Discharge"], "Eye Discharge"),
    "nasal discharge": (["Nasal_Discharge"], "Nasal Discharge"),
    "vomiting": (["Vomiting"], "Vomiting"),
    "diarrhea": (["Diarrhea"], "Diarrhea"),
    "lethargy": ([], "Lethargy"),
    "loss of appetite": (["Appetite_Loss"], "Appetite Loss"),
    "itching": (["Skin_Lesions"], "Skin Lesions"),
    "hair loss": (["Skin_Lesions"], "Skin Lesions"),
    "straining to urinate": (["Lameness"], "Lameness"),
    "blood in urine": ([], "Lethargy"),
    "weight loss": ([], "Weight Loss"),
    "excessive thirst": ([], "Lethargy"),
    "coughing": (["Coughing"], "Coughing"),
    "wheezing": (["Labored_Breathing"], "Labored Breathing"),
    "hiding behavior": ([], "Lethargy"),
    "pale gums": ([], "Fever"),
    "difficulty breathing": (["Labored_Breathing"], "Labored Breathing"),
}

_CAT_BASE_FOR_INTERACTION = (
    "Appetite_Loss",
    "Vomiting",
    "Diarrhea",
    "Coughing",
    "Labored_Breathing",
    "Lameness",
    "Skin_Lesions",
    "Nasal_Discharge",
    "Eye_Discharge",
)
_CAT_ANIMALS = ("Cat", "Cow", "Dog", "Goat", "Horse", "Pig", "Rabbit", "Sheep")


def _cat_classifier_feature_names() -> Optional[np.ndarray]:
    if CAT_CLASSIFIER is None:
        return None
    clf = CAT_CLASSIFIER.named_steps.get("clf")
    if clf is not None and hasattr(clf, "feature_names_in_"):
        return clf.feature_names_in_
    if hasattr(CAT_CLASSIFIER, "feature_names_in_"):
        return CAT_CLASSIFIER.feature_names_in_
    return None

def _build_livestock_features(
    symptoms: list[str],
    animal_type: str = "cow", 
    age: float = 3.0,
    temperature: float = 38.5,
) -> pd.DataFrame:
    
    row: dict[str, float] = {}

    row["Age"]         = float(age)
    row["Temperature"] = float(temperature)

    selected = {s.strip().lower() for s in symptoms}
    for col in _LIVESTOCK_SYMPTOM_COLS:
        row[col] = 1.0 if col in selected else 0.0

    # Animal one-hot
    target_col = f"Animal_{animal_type.lower()}"
    for col in _LIVESTOCK_ANIMAL_COLS:
        row[col] = 1.0 if col == target_col else 0.0

    col_order = (
        ["Age", "Temperature"]
        + _LIVESTOCK_SYMPTOM_COLS
        + _LIVESTOCK_ANIMAL_COLS
    )
    return pd.DataFrame([row], columns=col_order)


def _build_cat_features_dataframe(symptoms: list[str]) -> pd.DataFrame:
    """Build a single-row DataFrame matching the trained Pipeline’s 145 feature columns."""
    fn = _cat_classifier_feature_names()
    if fn is None:
        raise RuntimeError("Could not read feature_names_in_ from cat_model.joblib")

    row: dict[str, float] = {str(name): 0.0 for name in fn}
    row["Body_Temperature"] = 38.5
    row["Duration"] = 3.0
    for a in _CAT_ANIMALS:
        row[f"Animal_Type_{a}"] = 0.0
    row["Animal_Type_Cat"] = 1.0

    catalog = {s.lower(): s for s in SYMPTOMS["cat"]}
    slot_order: list[str] = []
    bases: set[str] = set()

    for raw in symptoms:
        key = raw.strip().lower()
        if key not in catalog:
            continue
        bases_flags, slot = _CAT_UI_TO_TRAINING.get(key, ([], "Lethargy"))
        bases.update(bases_flags)
        slot_order.append(slot)

    for b in bases:
        if b in row:
            row[b] = 1.0

    for i, slot in enumerate(slot_order[:4]):
        col = f"Symptom_{i + 1}_{slot}"
        if col in row:
            row[col] = 1.0

    for animal in _CAT_ANIMALS:
        at = row[f"Animal_Type_{animal}"]
        for b in _CAT_BASE_FOR_INTERACTION:
            ix = f"{animal}_x_{b}"
            if ix in row:
                row[ix] = at * row[b]

    return pd.DataFrame([row], columns=list(fn))


def _try_load_cat_classifier() -> Optional[object]:
    if not _CAT_MODEL_PATH.is_file():
        return None
    try:
        return joblib.load(_CAT_MODEL_PATH)
    except Exception:
        return None


CAT_CLASSIFIER = _try_load_cat_classifier()


def _resolve_cat_condition(pred: Any) -> str:
    if isinstance(pred, str):
        return pred
    try:
        pred_int = int(pred)
    except (TypeError, ValueError):
        return str(pred)
    if CAT_LABEL_ENCODER is not None:
        try:
            return decode_cat_labels([pred_int])[0]
        except (ValueError, IndexError):
            pass
    return str(pred)


_HIGH_URGENCY_KEYWORDS = frozenset({
    "labored breathing", "respiratory distress", "difficulty breathing",
    "pale gums", "seizure", "collapse", "poisoning", "urinary blockage",
    "cardiac", "heart failure", "flutd",
})
_HIGH_URGENCY_SYMPTOMS = frozenset({
    "labored_breathing", "difficulty breathing", "wheezing", "pale gums",
})
_LOW_URGENCY_KEYWORDS = frozenset({
    "minor", "mild", "sneezing",
})


def _cat_urgency(condition: str, symptoms: list[str], confidence: float) -> str:
    cond_lower = condition.lower()
    if any(kw in cond_lower for kw in _HIGH_URGENCY_KEYWORDS):
        return "high"
    sym_lower = {s.strip().lower() for s in symptoms}
    if sym_lower & _HIGH_URGENCY_SYMPTOMS:
        return "high"
    if any(kw in cond_lower for kw in _LOW_URGENCY_KEYWORDS):
        return "low"
    if confidence < 0.4:
        return "low"
    return "medium"


def _cat_model_result(symptoms: list[str]) -> dict:
    if CAT_CLASSIFIER is None:
        raise RuntimeError("Cat classifier not loaded")

    X = _build_cat_features_dataframe(symptoms)
    pred = CAT_CLASSIFIER.predict(X)[0]
    condition = _resolve_cat_condition(pred)

    confidence = 0.0
    if hasattr(CAT_CLASSIFIER, "predict_proba"):
        proba = CAT_CLASSIFIER.predict_proba(X)[0]
        confidence = float(np.max(proba))
    elif hasattr(CAT_CLASSIFIER, "decision_function"):
        confidence = 0.75

    return {
        "animal": "cat",
        "condition": condition,
        "confidence": round(confidence, 2),
        "urgency": _cat_urgency(condition, symptoms, confidence),
        "why": f"Predicted from your selected symptoms using the trained feline classifier (top class).",
        "next_steps": [
            "Consult a licensed veterinarian to confirm any concern.",
            "Keep a record of symptom onset and progression.",
        ],
        "matched_symptoms": symptoms,
        "red_flags": [],
        "model_version": "cat_model.joblib",
        "is_placeholder": False,
    }


def _cat_model_error(symptoms: list[str], message: str) -> dict:
    return {
        "animal": "cat",
        "condition": "Prediction unavailable",
        "confidence": 0.0,
        "urgency": "medium",
        "why": message,
        "next_steps": [
            "Ensure `cat_model.joblib` matches training (feature count and symptom order).",
            "Consult a licensed veterinarian for a proper diagnosis.",
        ],
        "matched_symptoms": symptoms,
        "red_flags": [],
        "model_version": "error",
        "is_placeholder": True,
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
    if CAT_CLASSIFIER is None:
        return _placeholder_result("cat", symptoms)
    try:
        return _cat_model_result(symptoms)
    except Exception as exc:
        return _cat_model_error(symptoms, str(exc))


def predict_livestock(
    symptoms: list[str],
    animal_type: str = "cow",
    age: float = 3.0,
    temperature: float = 38.5,
) -> dict:
    if LIVESTOCK_CLASSIFIER is None:
        return _placeholder_result("livestock", symptoms)

    try:
        X    = _build_livestock_features(symptoms, animal_type, age, temperature)
        pred = LIVESTOCK_CLASSIFIER.predict(X)[0]

        if LIVESTOCK_LABEL_ENCODER is not None:
            condition = str(LIVESTOCK_LABEL_ENCODER.inverse_transform([pred])[0])
        else:
            condition = str(pred)  

        confidence = 0.0
        if hasattr(LIVESTOCK_CLASSIFIER, "predict_proba"):
            proba      = LIVESTOCK_CLASSIFIER.predict_proba(X)[0]
            confidence = float(np.max(proba))
        elif hasattr(LIVESTOCK_CLASSIFIER, "decision_function"):
            confidence = 0.75

        return {
            "animal":     "livestock",
            "condition":  condition,
            "confidence": round(confidence, 2),
            "urgency":    "medium",
            "why":        "Predicted from selected symptoms using the trained livestock GradientBoosting classifier.",
            "next_steps": [
                "Consult a licensed veterinarian to confirm the diagnosis.",
                "Isolate the animal if an infectious disease is suspected.",
                "Record symptom onset, duration, and any recent environmental changes.",
            ],
            "matched_symptoms": symptoms,
            "red_flags":  [],
            "model_version": "livestock_model.joblib",
            "is_placeholder": False,
        }

    except Exception as exc:
        return {
            "animal":     "livestock",
            "condition":  "Prediction unavailable",
            "confidence": 0.0,
            "urgency":    "medium",
            "why":        f"Model error: {exc}",
            "next_steps": [
                "Ensure `livestock_model.joblib` and `livestock_label_encoder.joblib` "
                "are present and match training columns.",
                "Consult a licensed veterinarian for a proper diagnosis.",
            ],
            "matched_symptoms": symptoms,
            "red_flags":  [],
            "model_version": "error",
            "is_placeholder": True,
        }



# ---------------------------------------------------------------------------
# Model metadata — update once real models are in place
# ---------------------------------------------------------------------------
def _cat_training_status() -> str:
    if CAT_CLASSIFIER is not None:
        return "Classifier loaded (cat_model.joblib)"
    if CAT_LABEL_ENCODER is None:
        return "Awaiting real training data"
    n = len(cat_condition_names())
    return f"Label encoder ready ({n} disease classes); add cat_model.joblib for predictions"


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
        "version": "cat_model.joblib" if CAT_CLASSIFIER is not None else "0.0.0-placeholder",
        "status": "active" if CAT_CLASSIFIER is not None else "placeholder",
        "training_status": _cat_training_status(),
        "last_updated": "—",
        "accuracy": "N/A",
    },
    "livestock": {
        "name":            "Livestock Disease Classifier",
    "version":         "livestock_model.joblib" if LIVESTOCK_CLASSIFIER is not None else "0.0.0-placeholder",
    "status":          "active" if LIVESTOCK_CLASSIFIER is not None else "placeholder",
    "training_status": (
        "GradientBoostingClassifier loaded (livestock_model.joblib)"
        if LIVESTOCK_CLASSIFIER is not None
        else "Awaiting livestock_model.joblib"
    ),
    "last_updated": "—",
    "accuracy":     "N/A",
    },
}
