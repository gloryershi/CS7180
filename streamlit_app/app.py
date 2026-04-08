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
        """<div style="padding:0.45rem 0 0.9rem">
             <p class="sidebar-title">🐾 VetCheck</p>
             <p class="sidebar-subtitle">Animal Symptom Checker</p>
           </div>""",
        unsafe_allow_html=True,
    )

    animal = st.session_state.get("animal")
    if animal:
        icons = {"dog": "🐕", "cat": "🐈", "livestock": "🐄"}
        syms = st.session_state.get("symptoms", [])
        st.markdown(
            f"<div class='sidebar-card'><p style='margin:0;font-size:0.82rem;'>Current animal</p>"
            f"<p style='margin:0.15rem 0 0;font-size:1rem;font-weight:700;'>{icons.get(animal,'')} {animal.capitalize()}</p></div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div class='sidebar-card'><p style='margin:0;font-size:0.82rem;'>Symptoms selected</p>"
            f"<p style='margin:0.15rem 0 0;font-size:1rem;font-weight:700;'>{len(syms)}</p></div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            "<div class='sidebar-card'><p style='margin:0;font-size:0.86rem;'>Choose an animal on Home to begin the assessment flow.</p></div>",
            unsafe_allow_html=True,
        )

pages.run()
