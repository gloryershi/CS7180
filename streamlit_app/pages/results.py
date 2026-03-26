"""Results page — displays prediction, confidence, urgency, and next steps."""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.styles import inject_css, page_header, disclaimer, URGENCY_COLOR, URGENCY_LABEL

inject_css()

ANIMAL_ICONS = {"dog": "🐕", "cat": "🐈", "livestock": "🐄"}

page_header("📋 Assessment Results", "Review the likely condition and recommended next steps.")

# ── Guard ─────────────────────────────────────────────────────────────────
result = st.session_state.get("result")
if not result:
    st.info("No results yet. Complete the **Symptom Checker** first.")
    st.stop()

animal  = result.get("animal", "")
icon    = ANIMAL_ICONS.get(animal, "🐾")
urgency = result.get("urgency", "low")
conf    = result.get("confidence", 0.0)
is_ph   = result.get("is_placeholder", True)

# ── Top summary card ──────────────────────────────────────────────────────
urg_color = URGENCY_COLOR.get(urgency, "#52B788")
urg_label = URGENCY_LABEL.get(urgency, urgency.capitalize())
pill_html = (
    '<span class="pill-placeholder">⚠ Placeholder model</span>'
    if is_ph else
    '<span class="pill-final">✓ Production model</span>'
)

st.markdown(
    f"""<div class="card">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:0.5rem">
            <div>
              <p style="margin:0;font-size:0.85rem;color:#6B7280">Animal assessed</p>
              <h2 style="margin:0">{icon} {animal.capitalize()}</h2>
            </div>
            {pill_html}
          </div>
          <hr style="margin:1rem 0;border:none;border-top:1px solid #E5E7EB">
          <p style="margin:0;font-size:0.85rem;color:#6B7280">Top likely condition</p>
          <h3 style="margin:0.2rem 0 0.8rem;font-size:1.35rem">{result.get("condition","—")}</h3>
          <p style="margin:0 0 0.4rem;font-size:0.85rem;color:#6B7280">Model confidence</p>
          <div style="display:flex;align-items:center;gap:0.8rem">
            <div class="conf-bar-wrap" style="flex:1">
              <div class="conf-bar-fill" style="width:{int(conf*100)}%"></div>
            </div>
            <span style="font-weight:700;font-size:1rem">{int(conf*100)}%</span>
          </div>
          <div style="margin-top:0.9rem">
            <span class="badge badge-{urgency}">{urg_label}</span>
          </div>
        </div>""",
    unsafe_allow_html=True,
)

# ── Why this was suggested ────────────────────────────────────────────────
st.markdown("#### 🔎 Why this was suggested")
st.markdown(
    f'<div class="card"><p style="margin:0">{result.get("why","—")}</p></div>',
    unsafe_allow_html=True,
)

# ── Matched symptoms ──────────────────────────────────────────────────────
matched = result.get("matched_symptoms", [])
if matched:
    st.markdown("#### 🐾 Symptoms that matched this condition")
    st.markdown(
        "<div class='card'>" +
        "".join(f'<span style="display:inline-block;background:#D1FAE5;color:#065F46;'
                f'border-radius:999px;padding:0.2rem 0.8rem;margin:0.2rem;font-size:0.85rem">'
                f'{s}</span>' for s in matched) +
        "</div>",
        unsafe_allow_html=True,
    )

# ── Red flags ─────────────────────────────────────────────────────────────
red_flags = result.get("red_flags", [])
if red_flags:
    st.markdown("#### 🚨 Red-flag symptoms detected")
    st.error(
        "The following symptoms require **immediate veterinary attention**: " +
        ", ".join(red_flags)
    )

# ── Next steps ────────────────────────────────────────────────────────────
st.markdown("#### 🐾 Recommended next steps")
next_steps = result.get("next_steps", [])
for step in next_steps:
    st.markdown(
        f'<div class="card" style="padding:0.9rem 1.2rem;display:flex;gap:0.7rem;align-items:flex-start">'
        f'<span style="color:#2E7D5E;font-size:1.1rem">→</span>'
        f'<span>{step}</span></div>',
        unsafe_allow_html=True,
    )

# ── Entered symptoms recap ────────────────────────────────────────────────
entered = st.session_state.get("symptoms", [])
if entered:
    with st.expander("All symptoms entered"):
        for s in entered:
            st.markdown(f"- {s}")
    notes = st.session_state.get("notes", "").strip()
    if notes:
        with st.expander("Your additional notes"):
            st.write(notes)

# ── Results image ─────────────────────────────────────────────────────────
img_path = os.path.join(os.path.dirname(__file__), "..", "assets", "vet.png")
st.image(img_path, use_container_width=True)

# ── Re-check button ───────────────────────────────────────────────────────
st.markdown("---")
if st.button("🔄 Start a new assessment", use_container_width=True):
    for key in ("animal", "symptoms", "notes", "result"):
        st.session_state.pop(key, None)
    st.switch_page("pages/home.py")

disclaimer()