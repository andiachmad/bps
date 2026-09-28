# Panduan Struktur Modular - BPS Pulse

Modular = memecah program menjadi bagian kecil, masing-masing punya satu tugas dan satu tempat.

## Kerangka

```
codex/
├── main.py                  <- sutradara: menyambung semua modul
├── common/                  <- hal yang dipakai semua modul
│   └── settings.py          (path folder, API key)
├── ingest/                  <- MENGAMBIL data dari luar
│   ├── bps_client.py        (susun URL, panggil API)
│   └── save_raw.py          (simpan JSON mentah)
├── transform/               <- MENGOLAH data
│   ├── parse_dynamic.py     (JSON -> tabel)
│   └── clean.py             (rapikan tabel)
├── storage/      (nanti)    <- MENYIMPAN ke database (SQLite)
├── quality/      (nanti)    <- MENGECEK kualitas data asli
├── tests/                   <- MENGECEK kode benar (data palsu)
├── config/endpoints.yml     <- daftar endpoint
├── scripts/smoke_test.py    <- alat cek cepat API
├── data/raw, data/processed <- hasil (tidak di-commit)
└── docs/                    <- dokumentasi
```

## Tugas tiap folder

| Folder | Pertanyaan yang dijawab | Input -> Output |
|---|---|---|
| common | Di mana path dan key-nya? | - -> path, key |
| ingest | Bagaimana data diambil dan disimpan mentah? | URL -> JSON |
| transform | Bagaimana JSON jadi tabel rapi? | JSON -> DataFrame |
| storage | Di mana tabel disimpan permanen? | DataFrame -> database |
| quality | Apakah data asli masuk akal? | tabel -> lolos/gagal |
| tests | Apakah kodeku benar? | data palsu -> lolos/gagal |

`tests/` memeriksa KODE dengan data buatan. `quality/` memeriksa DATA ASLI hasil tarikan.

## Aturan 1: arah ketergantungan satu arah

```
main.py -> ingest, transform, storage, quality -> common
```

- main.py boleh memanggil semuanya.
- ingest tidak memanggil transform, dan sebaliknya.
- common tidak memanggil siapa pun.

## Aturan 2: menulis modul

1. Satu file, satu tugas.
2. Fungsi kecil dengan input dan output jelas.
3. Jangan tulis path atau key langsung di kode; ambil dari common/settings.py.
4. `print` hanya di main.py; modul lain mengembalikan nilai atau melempar error.
5. Setiap file punya docstring satu kalimat: "Tugas file ini: ...".
6. Data mentah (data/raw) tidak diubah setelah tersimpan.

## Aturan 3: menambah fitur baru (contoh Press Release)

1. ingest/bps_client.py: tambah fungsi penyusun URL.
2. transform/parse_press_release.py: file baru, JSON -> tabel.
3. tests/test_press_release.py: test dengan JSON palsu.
4. main.py: tambah satu langkah pemanggilan.

Urutan: ambil -> olah -> test -> sambungkan.

## Peta tahap belajar ke folder

| Tahap | Dikerjakan di |
|---|---|
| 1-2 (panggil API, baca JSON) | ingest/bps_client.py |
| 3 (jadi tabel) | transform/parse_dynamic.py |
| 4 (simpan mentah) | ingest/save_raw.py |
| 5 (bersihkan) | transform/clean.py |
| 6 (database) | storage/db.py |
| 7 (cek kualitas) | quality/checks.py |
| 8 (grafik/dashboard) | dashboard/ |
| 9 (otomatis) | scripts/ dan penjadwalan |

## Kesalahan umum pemula

- Menulis semuanya di satu file panjang.
- Menjalankan dari folder yang salah; selalu dari folder utama (`python main.py ...`, `python -m pytest`).
- Lupa `__init__.py` di folder paket.
- Meng-commit `.env` atau `data/raw`; keduanya harus tetap di `.gitignore`.