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

# ── Symptom search (outside form so it triggers live reruns) ──────────────
st.markdown("#### Search and select symptoms")
search = st.text_input("🔍 Filter symptoms (optional)", placeholder="e.g. vomiting, fever …")
filtered = [s for s in all_symptoms if search.lower() in s.lower()] if search else all_symptoms

# Keep previously selected symptoms in the options even if they don't match the search
current_selection = st.session_state.get("symptoms", [])
options = list(dict.fromkeys(current_selection + filtered))

# ── Symptom form ──────────────────────────────────────────────────────────
with st.form("symptom_form"):
    selected = st.multiselect(
        "Symptoms observed",
        options=options,
        default=[s for s in current_selection if s in options],
        help="Select all that apply. You can type to search.",
    )

    st.markdown("#### Additional notes *(optional)*")
    notes = st.text_area(
        "Describe anything else you've noticed",
        value=st.session_state.get("notes", ""),
        placeholder="e.g. started 2 days ago, no appetite since yesterday …",
        height=100,
    )

    submitted = st.form_submit_button("🔍 Run Assessment", use_container_width=True, type="primary")

# ── Validation + submit ───────────────────────────────────────────────────
if submitted:
    if len(selected) == 0:
        st.error("Please select at least one symptom before submitting.")
    else:
        st.session_state.symptoms = selected
        st.session_state.notes = notes

    with st.spinner("Running assessment …"):
        try:
            result = predict(animal, selected)
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