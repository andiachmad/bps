"""Tugas file ini: MENGUBAH JSON Dynamic Data menjadi tabel (DataFrame).

Kunci di 'datacontent' adalah gabungan kode:
    vervar + var + turvar + tahun + turtahun
Contoh: 9999 + 145 + 289 + 100 + 0 -> "99991452891000"
(Pola ini disimpulkan dari satu contoh, jadi divalidasi lewat test.)
"""
import itertools

import pandas as pd

# Dipakai bila respons tidak memuat turvar/turtahun
DEFAULT_ITEM = [{"val": 0, "label": ""}]


def parse_dynamic_data(js):
    var = js["var"][0]
    rows = []

    for v, t, y, ty in itertools.product(
        js.get("vervar", DEFAULT_ITEM),
        js.get("turvar", DEFAULT_ITEM),
        js.get("tahun", DEFAULT_ITEM),
        js.get("turtahun", DEFAULT_ITEM),
    ):
        key = f'{v["val"]}{var["val"]}{t["val"]}{y["val"]}{ty["val"]}'
        if key in js["datacontent"]:
            rows.append(
                {
                    "variabel": var["label"],
                    "satuan": var.get("unit", ""),
                    "wilayah": v["label"],
                    "kategori": t["label"],
                    "periode": y["label"],
                    "jenis_periode": ty["label"],
                    "nilai": js["datacontent"][key],
                }
            )
    return pd.DataFrame(rows)
