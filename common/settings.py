"""Pengaturan terpusat: lokasi folder dan pengambilan API key.

Semua file lain mengambil path dan key dari sini, jadi kalau ada yang
berubah cukup ubah di satu tempat.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

# parents[1] = naik satu tingkat dari common/ ke folder utama proyek
ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"

# Baca file .env di folder utama (isinya BPS_API_KEY=...)
load_dotenv(ROOT / ".env")


def get_api_key() -> str:
    """Ambil API key dari .env. Berhenti dengan pesan jelas bila belum diisi."""
    key = os.getenv("BPS_API_KEY", "").strip()
    if not key or key.startswith("isi_"):
        raise RuntimeError("BPS_API_KEY belum diisi di file .env")
    return key
