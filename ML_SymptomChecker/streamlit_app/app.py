"""
Main Streamlit entry point.
Run with: streamlit run streamlit_app/app.py
"""

import streamlit as st

st.set_page_config(
    page_title="VetCheck — Animal Symptom Checker",
    page_icon="🐾",
    layout="centered",
    initial_sidebar_state="expanded",
)

pages = st.navigation(
    {
        "": [
            st.Page("pages/home.py",            title="Home",             icon="🏠"),
        ],
        "Assessment": [
            st.Page("pages/symptom_checker.py", title="Symptom Checker",  icon="🩺"),
            st.Page("pages/results.py",         title="Results",          icon="📋"),
        ],
        "Info": [
            st.Page("pages/about_model.py",     title="About the Models", icon="🧠"),
            st.Page("pages/vet_disclaimer.py",  title="Vet Disclaimer",   icon="⚕️"),
        ],
    }
)

# ── Sidebar branding ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """<div style="padding:0.6rem 0 1.2rem">
             <p style="font-size:1.3rem;font-weight:700;margin:0">🐾 VetCheck</p>
             <p style="font-size:0.78rem;opacity:0.8;margin:0.2rem 0 0">Animal Symptom Checker</p>
           </div>""",
        unsafe_allow_html=True,
    )

    animal = st.session_state.get("animal")
    if animal:
        icons = {"dog": "🐕", "cat": "🐈", "livestock": "🐄"}
        st.markdown(
            f"<p style='font-size:0.82rem;opacity:0.85'>Current animal: "
            f"<strong>{icons.get(animal,'')} {animal.capitalize()}</strong></p>",
            unsafe_allow_html=True,
        )
        syms = st.session_state.get("symptoms", [])
        if syms:
            st.markdown(
                f"<p style='font-size:0.82rem;opacity:0.85'>Symptoms entered: "
                f"<strong>{len(syms)}</strong></p>",
                unsafe_allow_html=True,
            )

pages.run()
