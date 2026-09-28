"""Tugas file ini: MEMBERSIHKAN tabel hasil parse (layer 'clean')."""
import pandas as pd

TEXT_COLUMNS = ["variabel", "satuan", "wilayah", "kategori", "periode", "jenis_periode"]


def clean(df):
    df = df.copy()
    for col in TEXT_COLUMNS:
        df[col] = df[col].astype(str).str.strip()
    # Nilai yang tidak bisa jadi angka berubah menjadi kosong (NaN), bukan error
    df["nilai"] = pd.to_numeric(df["nilai"], errors="coerce")
    return df.drop_duplicates().reset_index(drop=True)
