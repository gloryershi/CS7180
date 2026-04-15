"""Thin wrapper around the Flask API."""

import requests

BASE_URL = "https://cs7180.onrender.com/api"
TIMEOUT = 10


def get_symptoms(animal: str) -> list[str]:
    resp = requests.get(f"{BASE_URL}/symptoms/{animal}", timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()["symptoms"]


def predict(animal: str, symptoms: list[str]) -> dict:
    resp = requests.post(
        f"{BASE_URL}/predict",
        json={"animal": animal, "symptoms": symptoms},
        timeout=TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()


def get_metadata() -> dict:
    resp = requests.get(f"{BASE_URL}/metadata", timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def health_check() -> bool:
    try:
        resp = requests.get(f"{BASE_URL}/health", timeout=3)
        return resp.status_code == 200
    except Exception:
        return False
