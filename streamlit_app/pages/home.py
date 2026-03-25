"""Home / Landing page — animal selector and workflow overview."""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.styles import inject_css, page_header, disclaimer
from utils.api import health_check

inject_css()

# ── Backend status ────────────────────────────────────────────────────────
backend_ok = health_check()
status_html = (
    '<span style="color:#34D399;font-weight:600">● API connected</span>'
    if backend_ok
    else '<span style="color:#F87171;font-weight:600">● API offline — start Flask first</span>'
)

page_header(
    "🐾 VetCheck — Animal Symptom Checker",
    "Describe your animal's symptoms and get an instant preliminary assessment.",
)
st.markdown(f"<p style='margin-top:-1rem;font-size:0.85rem'>{status_html}</p>", unsafe_allow_html=True)

img_path = os.path.join(os.path.dirname(__file__), "..", "assets", "kittens.jpg")
st.image(img_path, use_container_width=True)

# ── Animal selector ───────────────────────────────────────────────────────
st.markdown("<h3 style='text-align:center'>Select your animal to get started</h3>", unsafe_allow_html=True)

ANIMALS = {
    "dog":       ("🐕", "Dog",       "Canine Disease Classifier"),
    "cat":       ("🐈", "Cat",       "Feline Disease Classifier"),
    "livestock": ("🐄", "Livestock", "Livestock Disease Classifier"),
}

if "animal" not in st.session_state:
    st.session_state.animal = None

c1, c2, c3 = st.columns(3)
for col, (key, (icon, label, model_name)) in zip([c1, c2, c3], ANIMALS.items()):
    with col:
        selected = st.session_state.animal == key
        border = "#2E7D5E" if selected else "var(--vc-card-border)"
        shadow = "0 4px 20px rgba(46,125,94,0.25)" if selected else "none"

        st.markdown(
            f"""<div style="background:#fff;border:2px solid {border};border-radius:16px;
                            padding:1.6rem 1rem;text-align:center;box-shadow:{shadow}">
                  <span style="font-size:3rem">{icon}</span>
                  <p style="font-weight:700;margin:0.4rem 0 0.1rem">{label}</p>
                  <p style="font-size:0.78rem;color:#6B7280;margin:0">{model_name}</p>
                </div>""",
            unsafe_allow_html=True,
        )
    
        if st.button(f"Select {label}", key=f"sel_{key}", use_container_width=True):
            st.session_state.animal = key
            st.session_state.symptoms = []
            st.session_state.result = None
            st.switch_page("pages/symptom_checker.py")


# ── How it works ──────────────────────────────────────────────────────────
st.markdown("<h3 style='text-align:center'>How it works</h3>", unsafe_allow_html=True)
steps = [
    ("✔", "Choose animal",   "Select dog, cat, or livestock"),
    ("✔", "Enter symptoms",  "Pick from a searchable list"),
    ("🏁", "Get assessment",  "See likely conditions and urgency"),
    ("👩‍⚕️", "Next steps",      "Follow up with your vet for advice"),
]
cols = st.columns(4)
for col, (icon, title, desc) in zip(cols, steps):
    with col:
        st.markdown(
            f"""<div class="card" style="text-align:center;padding:1rem 0.8rem">
                  <span style="font-size:1.8rem">{icon}</span>
                  <p style="font-weight:700;margin:0.4rem 0 0.2rem">{title}</p>
                  <p style="font-size:0.82rem;color:#6B7280;margin:0">{desc}</p>
                </div>""",
            unsafe_allow_html=True,
        )

# ── CTA ───────────────────────────────────────────────────────────────────
if not st.session_state.animal:
    st.info("Select an animal above to begin.")

disclaimer()