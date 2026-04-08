"""Symptom Checker page — symptom form with session state and validation."""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.styles import inject_css, page_header, disclaimer
from utils.api import get_symptoms, predict, health_check

inject_css()

ANIMAL_ICONS = {"dog": "🐕", "cat": "🐈", "livestock": "🐄"}

# ── Animal-specific images ────────────────────────────────────────────────
ANIMAL_IMAGES = {
    "dog":       "puppy.png",
    "cat":       "kitten.jpg",
    "livestock": "livestock.png",
}

page_header("🩺 Symptom Checker", "Select all symptoms your animal is currently showing.")

# ── Guard: animal must be chosen first ───────────────────────────────────
animal = st.session_state.get("animal")
if not animal:
    st.warning("No animal selected. Please go to **Home** and choose an animal first.")
    st.stop()

icon = ANIMAL_ICONS.get(animal, "🐾")
st.markdown(
    f"<p>Checking for: <strong>{icon} {animal.capitalize()}</strong></p>",
    unsafe_allow_html=True,
)

# ── Animal image ──────────────────────────────────────────────────────────
img_file = ANIMAL_IMAGES.get(animal)
if img_file:
    img_path = os.path.join(os.path.dirname(__file__), "..", "assets", img_file)
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)

# ── Fetch symptom list ────────────────────────────────────────────────────
if not health_check():
    st.error("Flask API is not reachable. Start it with: `python flask_backend/app.py`")
    st.stop()

try:
    all_symptoms = get_symptoms(animal)
except Exception as e:
    st.error(f"Could not load symptoms: {e}")
    st.stop()

# ── Symptom picker (cleaner, first-time-user friendly) ────────────────────
st.markdown(
    """
    <style>
    .symptom-helper {
        color: #6B7280;
        margin-top: -0.35rem;
        margin-bottom: 0.7rem;
        font-size: 0.92rem;
    }
    .chip-note {
        color: #6B7280;
        font-size: 0.85rem;
        margin-bottom: 0.55rem;
    }
    div.stButton > button[kind="secondary"] {
        border-radius: 999px;
        min-height: 2.6rem;
        font-weight: 600;
        border: 1px solid #E5E7EB;
        background: #FFFFFF;
    }
    div.stButton > button[kind="secondary"]:hover {
        border-color: #52B788;
        color: #2E7D5E;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def _add_symptom(symptom: str) -> None:
    if symptom and symptom not in st.session_state.symptoms:
        st.session_state.symptoms.append(symptom)


def _common_symptoms_for(selected_animal: str, symptoms: list[str]) -> list[str]:
    preferred = {
        "dog": ["Vomiting", "Diarrhea", "Lethargy", "Loss of appetite", "Coughing", "Itching"],
        "cat": ["Vomiting", "Diarrhea", "Lethargy", "Loss of appetite", "Sneezing", "Eye discharge"],
        "livestock": ["Fever", "Limping", "Bloating", "Loss of appetite", "Diarrhea", "Coughing"],
    }
    chosen = [s for s in preferred.get(selected_animal, []) if s in symptoms]
    return chosen if chosen else symptoms[:6]


if "symptoms" not in st.session_state:
    st.session_state.symptoms = []

title_animal = f"{animal}'s" if not animal.endswith("s") else f"{animal}'"
st.markdown("### 1) Select symptoms")
st.markdown(
    f"<p class='symptom-helper'>Start with your {title_animal} most obvious symptom, then add any others you've noticed.</p>",
    unsafe_allow_html=True,
)
main_picker_key = f"main_symptom_pick_{animal}"
main_symptom = st.selectbox(
    "Choose main symptom",
    options=all_symptoms,
    index=None,
    placeholder="Choose a symptom...",
    label_visibility="collapsed",
    key=main_picker_key,
)
if st.button("Add main symptom", use_container_width=True, disabled=main_symptom is None):
    _add_symptom(main_symptom)

st.markdown("#### Common symptoms")
st.markdown("<p class='chip-note'>Quick-add options:</p>", unsafe_allow_html=True)
common_symptoms = _common_symptoms_for(animal, all_symptoms)
chip_cols = st.columns(3)
for i, sym in enumerate(common_symptoms):
    with chip_cols[i % 3]:
        if st.button(
            f"+ {sym}",
            key=f"quick_{animal}_{sym}",
            use_container_width=True,
            disabled=sym in st.session_state.symptoms,
        ):
            _add_symptom(sym)

st.markdown("#### Add another symptom (optional)")
extra_picker_key = f"extra_symptom_pick_{animal}"
extra_symptom = st.selectbox(
    "Add another symptom",
    options=all_symptoms,
    index=None,
    placeholder="Choose a symptom...",
    label_visibility="collapsed",
    key=extra_picker_key,
)
if st.button("Add selected symptom", use_container_width=True, disabled=extra_symptom is None):
    _add_symptom(extra_symptom)

st.markdown("### 2) Review selected symptoms")
selected = st.multiselect(
    "Selected symptoms",
    options=all_symptoms,
    default=st.session_state.symptoms,
    help="You can remove any symptom before running the assessment.",
)
st.session_state.symptoms = selected

st.markdown("### 3) Add notes and run")
notes = st.text_area(
    "Describe anything else you've noticed",
    value=st.session_state.get("notes", ""),
    placeholder="e.g. started 2 days ago, no appetite since yesterday ...",
    height=100,
)

submitted = st.button("🔍 Run Assessment", use_container_width=True, type="primary")

# ── Validation + submit ───────────────────────────────────────────────────
if submitted:
    if len(st.session_state.symptoms) == 0:
        st.error("Please select at least one symptom before submitting.")
    else:
        st.session_state.notes = notes
        with st.spinner("Running assessment ..."):
            try:
                result = predict(animal, st.session_state.symptoms)
                st.session_state.result = result
                st.switch_page("pages/results.py")
            except Exception as e:
                st.error(f"Prediction failed: {e}")

# ── Current selection summary (shown before first submit) ────────────────
if st.session_state.get("symptoms"):
    st.markdown("---")
    st.markdown("**Currently selected symptoms:**")
    cols = st.columns(3)
    for i, sym in enumerate(st.session_state.symptoms):
        cols[i % 3].markdown(f"- {sym}")

disclaimer()