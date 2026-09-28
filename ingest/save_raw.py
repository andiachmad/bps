"""Tugas file ini: MENYIMPAN JSON mentah apa adanya (layer 'raw')."""
import json
from datetime import datetime, timezone

from common.settings import RAW_DIR


def save_raw_json(name, data):
    """Simpan data ke data/raw/<name>_<waktu>.json dan kembalikan path-nya."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = RAW_DIR / f"{name}_{stamp}.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return path
