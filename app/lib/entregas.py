"""Envío de tareas al web app de Google Apps Script (guarda en Drive y registra en Sheets).

La URL y el token viven en los secrets de Streamlit, nunca en el repo:

    [entregas]
    url = "https://script.google.com/macros/s/…/exec"
    token = "…"
"""
import base64
import re

import requests
import streamlit as st

MAX_MB = 10
TIPOS = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "pdf": "application/pdf"}
CORREO_OK = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def config() -> dict | None:
    """Secrets de entregas, o None si aún no se configuraron."""
    try:
        cfg = st.secrets["entregas"]
        if cfg.get("url") and cfg.get("token"):
            return {"url": cfg["url"], "token": cfg["token"]}
    except Exception:  # sin secrets.toml o sin la sección [entregas]
        pass
    return None


def validar(nombre: str, correo: str, archivo, confirmo: bool) -> str | None:
    """Mensaje de error para el alumno, o None si todo está bien."""
    if len(nombre.strip()) < 3:
        return "Escribe tu nombre completo."
    if not CORREO_OK.match(correo.strip()):
        return "Revisa tu correo: parece que le falta algo."
    if archivo is None:
        return "Sube la imagen o el PDF de tu dashboard."
    ext = archivo.name.rsplit(".", 1)[-1].lower()
    if ext not in TIPOS:
        return "El archivo debe ser PNG, JPG o PDF."
    if archivo.size > MAX_MB * 1024 * 1024:
        return f"El archivo pesa {archivo.size / 1024 / 1024:.1f} MB; el máximo es {MAX_MB} MB."
    if not confirmo:
        return "Marca la casilla para confirmar que es tu trabajo."
    return None


def submit(cfg: dict, nombre: str, correo: str, archivo) -> tuple[bool, str]:
    """Manda la tarea al Apps Script. Devuelve (ok, mensaje para el alumno)."""
    ext = archivo.name.rsplit(".", 1)[-1].lower()
    payload = {
        "token": cfg["token"],
        "nombre": nombre.strip(),
        "correo": correo.strip(),
        "filename": archivo.name,
        "mimetype": TIPOS[ext],
        "data": base64.b64encode(archivo.getvalue()).decode("ascii"),
    }
    try:
        r = requests.post(cfg["url"], json=payload, timeout=60)
        r.raise_for_status()
        resp = r.json()
    except requests.RequestException:
        return False, "No pudimos conectar con el servidor de entregas. Intenta de nuevo en unos minutos."
    except ValueError:
        return False, "El servidor de entregas respondió algo inesperado. Avísale a tu profesor."
    if resp.get("ok"):
        return True, resp.get("hora", "")
    return False, resp.get("error", "La entrega fue rechazada. Avísale a tu profesor.")
