import argparse

from common.settings import PROCESSED_DIR, get_api_key
from ingest.bps_client import build_data_url, fetch_json
from ingest.save_raw import save_raw_json
from transform.clean import clean
from transform.parse_dynamic import parse_dynamic_data


def run(domain, var, th=None, turvar=None, vervar=None):
    key = get_api_key()

    url = build_data_url(key, domain, var, th=th, turvar=turvar, vervar=vervar)
    js = fetch_json(url)                                  # 1. ambil
    raw_path = save_raw_json(f"data_{domain}_{var}", js)  # 2. simpan mentah
    df = clean(parse_dynamic_data(js))                    # 3-4. parse + bersihkan

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    out = PROCESSED_DIR / f"data_{domain}_{var}.csv"
    df.to_csv(out, index=False)                           # 5. simpan hasil

    print(f"Mentah : {raw_path}")
    print(f"Bersih : {out}  ({len(df)} baris)")
    print(df.head())
    return df


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Tarik satu tabel Dynamic Data BPS")
    p.add_argument("--var", required=True, help="ID variabel")
    p.add_argument("--domain", default="0000", help="Kode domain (0000 = nasional)")
    p.add_argument("--th", help="ID periode")
    p.add_argument("--turvar", help="ID variabel turunan")
    p.add_argument("--vervar", help="ID variabel vertikal")
    a = p.parse_args()
    run(a.domain, a.var, th=a.th, turvar=a.turvar, vervar=a.vervar)
