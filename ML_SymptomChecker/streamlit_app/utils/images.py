"""
Image path resolver.
Drop your own files into streamlit_app/assets/ and they will be used automatically.
If a local file is missing the placeholder URL is used as a fallback.
"""

import os

_ASSETS = os.path.join(os.path.dirname(__file__), "..", "assets")


def _resolve(filename: str, fallback: str) -> str:
    path = os.path.join(_ASSETS, filename)
    return path if os.path.exists(path) else fallback


# ── Image registry ────────────────────────────────────────────────────────
# Replace fallback URLs with real ones, or just drop files into assets/.
IMAGES = {
    # Full-width hero banner on the Home page
    "hero": _resolve(
        "hero.jpg",
        "https://placehold.co/860x260/2E7D5E/ffffff?text=VetCheck+%E2%80%94+Animal+Symptom+Checker",
    ),
    # Animal card thumbnails
    "dog": _resolve(
        "dog.jpg",
        "https://placehold.co/400x220/52B788/ffffff?text=Dog",
    ),
    "cat": _resolve(
        "cat.jpg",
        "https://placehold.co/400x220/52B788/ffffff?text=Cat",
    ),
    "livestock": _resolve(
        "livestock.jpg",
        "https://placehold.co/400x220/52B788/ffffff?text=Livestock",
    ),
    # Results page — vet consultation illustration
    "vet": _resolve(
        "vet.jpg",
        "https://placehold.co/860x180/457B9D/ffffff?text=Consult+a+Veterinarian",
    ),
}
