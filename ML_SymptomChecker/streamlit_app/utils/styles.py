"""Shared CSS injected into every Streamlit page."""

import streamlit as st

PALETTE = {
    "primary":    "#2E7D5E",   # deep green
    "secondary":  "#52B788",   # mid green
    "accent":     "#F4A261",   # warm orange
    "critical":   "#E63946",
    "high":       "#F4A261",
    "medium":     "#457B9D",
    "low":        "#52B788",
    "surface":    "#F8FAF9",
    "card":       "#FFFFFF",
    "text":       "#1C1C1E",
    "muted":      "#6B7280",
}

URGENCY_COLOR = {
    "critical": PALETTE["critical"],
    "high":     PALETTE["high"],
    "medium":   PALETTE["medium"],
    "low":      PALETTE["low"],
}

URGENCY_LABEL = {
    "critical": "🚨 Emergency — see a vet immediately",
    "high":     "⚠️  High — vet visit within 24 hours",
    "medium":   "📅 Medium — schedule a vet appointment",
    "low":      "🟢 Low — monitor and consult if worsens",
}


def inject_css():
    st.markdown(
        f"""
        <style>
        /* ── Global ── */
        html, body, [class*="css"] {{
            font-family: 'Inter', 'Segoe UI', sans-serif;
            color: {PALETTE['text']};
        }}
        .main .block-container {{
            padding-top: 2rem;
            max-width: 860px;
        }}

        /* ── Sidebar ── */
        section[data-testid="stSidebar"] {{
            background: {PALETTE['primary']};
        }}
        section[data-testid="stSidebar"] * {{
            color: #fff !important;
        }}
        section[data-testid="stSidebar"] .stRadio label {{
            color: #fff !important;
        }}

        /* ── Page header banner ── */
        .page-header {{
            background: linear-gradient(135deg, {PALETTE['primary']} 0%, {PALETTE['secondary']} 100%);
            border-radius: 16px;
            padding: 2.2rem 2rem 1.8rem 2rem;
            color: #fff;
            margin-bottom: 1.8rem;
        }}
        .page-header h1 {{ margin: 0; font-size: 2rem; font-weight: 700; }}
        .page-header p  {{ margin: 0.4rem 0 0; font-size: 1.05rem; opacity: 0.9; }}

        /* ── Cards ── */
        .card {{
            background: {PALETTE['card']};
            border-radius: 14px;
            padding: 1.4rem 1.6rem;
            box-shadow: 0 2px 12px rgba(0,0,0,0.07);
            margin-bottom: 1.2rem;
        }}
        .card h3 {{ margin: 0 0 0.5rem; font-size: 1.1rem; color: {PALETTE['primary']}; }}

        /* ── Urgency badge ── */
        .badge {{
            display: inline-block;
            border-radius: 999px;
            padding: 0.3rem 1rem;
            font-size: 0.85rem;
            font-weight: 600;
            color: #fff;
        }}
        .badge-critical {{ background: {PALETTE['critical']}; }}
        .badge-high     {{ background: {PALETTE['high']}; color: #1C1C1E; }}
        .badge-medium   {{ background: {PALETTE['medium']}; }}
        .badge-low      {{ background: {PALETTE['low']}; }}

        /* ── Confidence bar ── */
        .conf-bar-wrap {{
            background: #E8F5EF;
            border-radius: 999px;
            height: 10px;
            width: 100%;
            overflow: hidden;
        }}
        .conf-bar-fill {{
            height: 100%;
            border-radius: 999px;
            background: linear-gradient(90deg, {PALETTE['secondary']}, {PALETTE['primary']});
        }}

        /* ── Animal selector cards ── */
        .animal-card {{
            background: {PALETTE['card']};
            border: 2px solid #E5E7EB;
            border-radius: 16px;
            padding: 1.8rem 1rem;
            text-align: center;
            cursor: pointer;
            transition: border-color .2s, box-shadow .2s;
        }}
        .animal-card:hover {{
            border-color: {PALETTE['secondary']};
            box-shadow: 0 4px 20px rgba(46,125,94,0.15);
        }}
        .animal-card.selected {{
            border-color: {PALETTE['primary']};
            box-shadow: 0 4px 20px rgba(46,125,94,0.25);
        }}
        .animal-card span {{ font-size: 3rem; display: block; }}
        .animal-card p    {{ margin: 0.5rem 0 0; font-weight: 600; color: {PALETTE['text']}; }}

        /* ── Disclaimer box ── */
        .disclaimer {{
            background: #FFF8F0;
            border-left: 4px solid {PALETTE['accent']};
            border-radius: 8px;
            padding: 1rem 1.2rem;
            font-size: 0.9rem;
            color: #7A5C3A;
            margin-top: 1.2rem;
        }}

        /* ── Placeholder badge ── */
        .pill-placeholder {{
            display:inline-block; background:#FFF3CD; color:#856404;
            border:1px solid #FFECB5; border-radius:999px;
            padding:0.15rem 0.75rem; font-size:0.78rem; font-weight:600;
        }}
        .pill-final {{
            display:inline-block; background:#D1FAE5; color:#065F46;
            border:1px solid #A7F3D0; border-radius:999px;
            padding:0.15rem 0.75rem; font-size:0.78rem; font-weight:600;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_header(title: str, subtitle: str = ""):
    st.markdown(
        f"""<div class="page-header">
              <h1>{title}</h1>
              {'<p>' + subtitle + '</p>' if subtitle else ''}
            </div>""",
        unsafe_allow_html=True,
    )


def card(content_html: str):
    st.markdown(f'<div class="card">{content_html}</div>', unsafe_allow_html=True)


def disclaimer():
    st.markdown(
        """<div class="disclaimer">
           ⚕️ <strong>Not a diagnosis.</strong> This tool is for informational purposes only
           and does not replace professional veterinary advice. Always consult a licensed
           veterinarian before making any health decisions for your animal.
           </div>""",
        unsafe_allow_html=True,
    )
