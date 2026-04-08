"""About Model page — displays metadata for all three models."""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.styles import inject_css, page_header
from utils.api import get_metadata, health_check

inject_css()

page_header("🧠 About the Models", "Technical details and status of each prediction model.")

if not health_check():
    st.error("Flask API is not reachable. Start it with: `python flask_backend/app.py`")
    st.stop()

try:
    metadata = get_metadata()
except Exception as e:
    st.error(f"Could not load metadata: {e}")
    st.stop()

ICONS = {"dog": "", "cat": "🐈", "livestock": "🐄"}

for animal, meta in metadata.items():
    icon = ICONS.get(animal, "🐾")
    status = meta.get("status", "unknown")
    is_placeholder = status == "placeholder"
    pill = (
        '<span class="pill-placeholder">⚠ Placeholder</span>'
        if is_placeholder else
        '<span class="pill-final">✓ Production</span>'
    )
    st.markdown(
        f"""<div class="card">
              <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.5rem">
                <h3 style="margin:0">{icon} {animal.capitalize()} — {meta.get("name","—")}</h3>
                {pill}
              </div>
              <table style="margin-top:0.8rem;width:100%;border-collapse:collapse;font-size:0.9rem">
                <tr>
                  <td style="padding:0.3rem 0.8rem 0.3rem 0;color:#6B7280;width:40%">Version</td>
                  <td style="font-weight:600">{meta.get("version","—")}</td>
                </tr>
                <tr>
                  <td style="padding:0.3rem 0.8rem 0.3rem 0;color:#6B7280">Training status</td>
                  <td style="font-weight:600">{meta.get("training_status","—")}</td>
                </tr>
                <tr>
                  <td style="padding:0.3rem 0.8rem 0.3rem 0;color:#6B7280">Last updated</td>
                  <td style="font-weight:600">{meta.get("last_updated","—")}</td>
                </tr>
                <tr>
                  <td style="padding:0.3rem 0.8rem 0.3rem 0;color:#6B7280">Accuracy</td>
                  <td style="font-weight:600">{meta.get("accuracy","—")}</td>
                </tr>
              </table>
            </div>""",
        unsafe_allow_html=True,
    )