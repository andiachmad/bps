"""Tugas file ini: MENGAMBIL data dari API BPS. Tidak mengolah isinya."""
import requests

BASE_URL = "https://webapi.bps.go.id/v1/api/list"
USER_AGENT = "Mozilla/5.0 (compatible; bps-pulse/0.1)"


def build_data_url(key, domain, var, th=None, turvar=None, vervar=None, lang="ind"):
    """Susun URL Dynamic Data (model 'data').

    Parameter wajib: key, domain, var. Sisanya opsional.
    CATATAN: pola URL ini disusun dari dokumentasi BPS, cocokkan dengan
    tombol 'Try it' di https://webapi.bps.go.id/documentation/
    """
    parts = ["model/data", f"lang/{lang}", f"domain/{domain}", f"var/{var}"]
    if th is not None:
        parts.append(f"th/{th}")
    if turvar is not None:
        parts.append(f"turvar/{turvar}")
    if vervar is not None:
        parts.append(f"vervar/{vervar}")
    parts.append(f"key/{key}")
    return BASE_URL + "/" + "/".join(parts) + "/"


def fetch_json(url, timeout=30):
    """Panggil URL dan kembalikan JSON (dictionary Python).

    Pesan error sengaja tidak memuat URL supaya API key tidak bocor.
    """
    try:
        resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=timeout)
    except requests.RequestException as e:
        raise RuntimeError(f"Gagal terhubung ke API ({type(e).__name__})") from None

    if resp.status_code == 403 or "Just a moment" in resp.text:
        raise RuntimeError("Diblokir (403/Cloudflare). Coba dari jaringan lain.")
    if resp.status_code != 200:
        raise RuntimeError(f"API membalas HTTP {resp.status_code}")

    try:
        js = resp.json()
    except ValueError:
        raise RuntimeError("Respons bukan JSON") from None

    if js.get("status") != "OK":
        raise RuntimeError(f"Status API bukan OK: {js.get('status')}")
    return js
