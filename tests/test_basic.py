"""Test dasar tanpa internet. Jalankan dari folder utama:  python -m pytest -q"""
from ingest.bps_client import build_data_url
from transform.clean import clean
from transform.parse_dynamic import parse_dynamic_data

# JSON palsu dengan bentuk yang sama seperti respons BPS
FAKE = {
    "status": "OK",
    "var": [{"val": 145, "label": "Persentase Rumah Tangga", "unit": "Persen"}],
    "turvar": [{"val": 289, "label": "Listrik PLN"}],
    "vervar": [{"val": 9999, "label": "INDONESIA"}, {"val": 1100, "label": "ACEH"}],
    "tahun": [{"val": 100, "label": "2000"}],
    "turtahun": [{"val": 0, "label": "Tahun"}],
    "datacontent": {"99991452891000": 83.68, "11001452891000": " 70.5"},
}


def test_build_url_wajib_dan_opsional():
    url = build_data_url("KUNCI", "0000", 145, th=100)
    assert "domain/0000" in url and "var/145" in url and "th/100" in url
    assert url.endswith("key/KUNCI/")
    assert "turvar" not in url  # opsional tidak ikut bila tidak diisi


def test_parse_jumlah_dan_nilai():
    df = parse_dynamic_data(FAKE)
    assert len(df) == 2
    nasional = df[df["wilayah"] == "INDONESIA"].iloc[0]
    assert nasional["nilai"] == 83.68
    assert nasional["kategori"] == "Listrik PLN"
    assert nasional["periode"] == "2000"


def test_clean_ubah_ke_angka():
    df = clean(parse_dynamic_data(FAKE))
    assert df["nilai"].dtype.kind == "f"          # angka desimal
    assert df.loc[df["wilayah"] == "ACEH", "nilai"].iloc[0] == 70.5
